# Darkwing: Let's get IP-rangerous!
# Copyright (C) 2020 Mark E. Haase <mehaase@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from base64 import b64decode
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
import logging
import typing

from lxml import etree
import trio

from . import dispatch
from ..database.scan import get_host_scan, insert_host_scan, list_host_scans
from ..model.host import Host, Hostname, HostState, Port, PortState, Service, Transport
from ..model.scan import HostScan


logger = logging.getLogger(__name__)


@dispatch.handler
async def upload_scan(base64_data: str) -> dict:
    data = b64decode(base64_data.encode("utf8"))
    scan = await trio.to_thread.run_sync(parse_nmap, data)
    scan_id = await insert_host_scan(dispatch.ctx.db, scan)
    return {"scan_id": scan_id}


@dispatch.handler
async def list_scans() -> dict:
    return {"scans": await list_host_scans(dispatch.ctx.db)}


@dispatch.handler
async def get_scan(scan_id: str) -> dict:
    return await get_host_scan(dispatch.ctx.db, scan_id)


def parse_nmap(xml_data: bytes) -> HostScan:
    nmaprun = etree.fromstring(xml_data)
    scan = HostScan("nmap", nmaprun.get("version"))
    scan.command_line = nmaprun.get("args")
    scan.started = datetime.fromtimestamp(int(nmaprun.get("start")))

    for child in nmaprun:
        if child.tag == "host":
            scan.hosts.append(parse_nmap_host(child))

    return scan


def parse_nmap_host(host_el: etree.Element) -> Host:
    host = Host()
    host.started = datetime.fromtimestamp(int(host_el.get("starttime")))
    host.completed = datetime.fromtimestamp(int(host_el.get("endtime")))

    for child in host_el:
        if child.tag == "status":
            host.state = HostState.UP if child.get("state") == "up" else HostState.DOWN
            host.state_reason = child.get("reason")
        elif child.tag == "address":
            if child.get("addrtype") == "ipv4":
                host.addresses.append(IPv4Address(child.get("addr")))
            else:
                host.addresses.append(IPv6Address(child.get("addr")))
        elif child.tag == "hostnames":
            for hostname_el in child:
                host.hostnames.append(
                    Hostname(hostname_el.get("name"), hostname_el.get("type"))
                )
        elif child.tag == "ports":
            for port_el in child:
                if port_el.tag == "port":
                    host.ports.append(parse_nmap_port(port_el))

    return host


def parse_nmap_port(port_el: etree.Element) -> Port:
    number = int(port_el.get("portid"))
    transport = Transport.from_nmap_str(port_el.get("protocol"))
    port = Port(number, transport)

    for child in port_el:
        if child.tag == "state":
            port.state = PortState.from_nmap_str(child.get("state"))
            port.state_reason = child.get("reason")
        elif child.tag == "service":
            service = Service(child.get("name"))
            service.product = child.get("product")
            service.version = child.get("version")
            service.method = child.get("method")
            service.confidence = int(child.get("conf"))
            for cpe in child:
                if cpe.tag == "cpe":
                    service.cpes.append(cpe.text.strip())
            port.service = service

    return port
