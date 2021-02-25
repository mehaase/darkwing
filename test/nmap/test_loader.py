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
from ipaddress import IPv4Address
from pathlib import Path

from darkwing.model.host import HostState, PortState, Transport
from darkwing.nmap.loader import load_scan


def test_load_scan():
    fixture_path = Path(__file__).absolute().parent / "test-scan.xml"
    with fixture_path.open("r") as fixture:
        scan = load_scan(fixture.read())
    assert scan.scanner == "nmap"
    assert scan.scanner_version == "7.80"
    assert scan.command_line == "nmap -A -sV -oX test-scan.xml 219.70.91.228/24"
    assert scan.started == datetime(2020, 4, 21, 14, 35, 12)
    assert scan.completed == datetime(2020, 4, 21, 14, 58, 7)

    assert len(scan.hosts) == 27
    host = scan.hosts[0]
    assert host.started == datetime(2020, 4, 21, 14, 35, 12)
    assert host.completed == datetime(2020, 4, 21, 14, 58, 7)
    assert host.state == HostState.UP
    assert host.state_reason == "conn-refused"

    assert len(host.addresses) == 1
    assert host.addresses[0] == IPv4Address("219.70.91.9")

    assert len(host.hostnames) == 1
    assert host.hostnames[0] == "219-70-91-9.hyabd.com.tw"

    assert len(host.ports) == 9
    port0 = host.ports[0]
    assert port0.number == 19
    assert port0.transport == Transport.TCP
    assert port0.state == PortState.FILTERED
    assert port0.state_reason == "host-unreach"
    assert port0.service.name == "chargen"
    assert port0.service.product is None
    assert port0.service.version is None

