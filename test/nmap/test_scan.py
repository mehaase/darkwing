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

from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path

from darkwing.model.host import HostState, PortState, Transport
from darkwing.server.scan import parse_nmap


here = Path(__file__).resolve().parent


def test_parse_nmap_jhu():
    """ This is a basic port scan. """
    nmap_jhu = here / "nmap-jhu.xml"
    with nmap_jhu.open("rb") as nmap_jhu_file:
        scan = parse_nmap(nmap_jhu_file.read())
    assert scan.scanner == "nmap"
    assert scan.scanner_version == "7.80"
    assert scan.command_line == "nmap -oX jhu.xml 128.220.176.140/24"
    assert len(scan.hosts) == 3
    host0 = scan.hosts[0]
    assert host0.started == datetime(2020, 4, 21, 8, 54, 45)
    assert host0.started == datetime(2020, 4, 21, 8, 54, 45)
    assert host0.completed == datetime(2020, 4, 21, 8, 54, 55)
    assert host0.state == HostState.UP
    assert host0.state_reason == "syn-ack"
    assert host0.addresses[0] == IPv4Address("128.220.176.12")
    assert len(host0.hostnames) == 0
    assert len(host0.ports) == 4
    port0 = host0.ports[0]
    assert port0.number == 22
    assert port0.transport == Transport.TCP
    assert port0.state == PortState.OPEN
    assert port0.state_reason == "syn-ack"
    assert port0.service.name == "ssh"
    assert port0.service.product is None
    port3 = host0.ports[3]
    assert port3.number == 8080
    assert port3.state == PortState.CLOSED
    assert port3.state_reason == "conn-refused"


def test_parse_nmap_hoshin():
    """ This port scan has host names, OS detection, and service detection. """
    nmap_hoshin = here / "nmap-hoshin.xml"
    with nmap_hoshin.open("rb") as nmap_hoshin_file:
        scan = parse_nmap(nmap_hoshin_file.read())
    assert scan.scanner == "nmap"
    assert scan.scanner_version == "7.80"
    assert scan.command_line == "nmap -A -sV -oX hosin.xml 219.70.91.228/24"
    assert len(scan.hosts) == 27
    host0 = scan.hosts[0]
    assert len(host0.hostnames) == 1
    hostname0 = host0.hostnames[0]
    assert hostname0.name == "219-70-91-9.hyabd.com.tw"
    assert hostname0.type_ == "PTR"
    assert len(host0.ports) == 9
    port0 = host0.ports[0]
    assert port0.number == 19
    assert port0.state == PortState.FILTERED
    assert port0.state_reason == "host-unreach"
    port1 = host0.ports[1]
    assert port1.number == 22
    assert port1.state == PortState.OPEN
    assert port1.state_reason == "syn-ack"
    service = port1.service
    assert service.name == "ssh"
    assert service.product == "Dropbear sshd"
    assert service.version == "2012.55"
    assert service.method == "probed"
    assert service.confidence == 10
    assert service.cpes == [
        "cpe:/a:matt_johnston:dropbear_ssh_server:2012.55",
        "cpe:/o:linux:linux_kernel",
    ]
