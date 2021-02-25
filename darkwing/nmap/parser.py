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
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
import typing
import xml.sax


class NmapXmlParseException(Exception):
    """ Indicates an error while parsing Nmap XML. """


class NmapXmlParser(xml.sax.handler.ContentHandler):
    """
    A streaming nmap parser.

    You feed bits of XML to this parser, and it will generate corresponding events. This
    can be used to parse very large nmap files efficiently, to parse nmap files in
    real-time while the scanner is still running, or to parse a file while concurrently
    streaming it over a network connection.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._capture_text = None
        self._current_host = None
        self._current_port = None
        self._current_script = None
        self._current_script_name = None
        self._current_script_key = None
        self._events = deque()
        self._stack = list()
        self._parser = xml.sax.make_parser()
        self._parser.setContentHandler(self)

    def feed(self, data):
        """
        Feed data into the parser.
        """
        self._parser.feed(data)

    def startElement(self, name, attrs):
        """
        This event indicates the start of an XML element. (Part of SAX API)
        """
        try:
            callback = getattr(self, f"_start_{name}")
        except AttributeError:
            return
        callback(attrs)

    def endElement(self, name):
        """
        This event indicates the end of an XML element. (Part of SAX API)
        """
        try:
            callback = getattr(self, f"_stop_{name}")
        except AttributeError:
            return
        callback()

    def characters(self, content):
        """
        Capture data from text nodes if capture currently enabled. (Part of SAX API)
        """
        if self._capture_text is not None:
            self._capture_text += content

    def start_text_capture(self):
        """ Start capturing data from text nodes. """
        if self._capture_text is not None:
            raise NmapXmlParseException(
                "start_text_capture() called but capture is already on!"
            )
        self._capture_text = ""

    def stop_text_capture(self):
        """ Stop capturing data from text nodes and return the current capture. """
        if self._capture_text is None:
            raise NmapXmlParseException(
                "stop_text_capture() called but capture is already off!"
            )
        text = self._capture_text
        self._capture_text = None
        return text

    def events(self):
        """
        This generator yields high-level events from the parsed XML stream.
        """
        while self._events:
            event = self._events.popleft()
            yield event

    def _start_nmaprun(self, attrs):
        """
        Create an NmapRun from an <nmaprun> element.
        """
        self._events.append(
            NmapRun(
                attrs["scanner"],
                attrs["version"],
                attrs["args"],
                datetime.utcfromtimestamp(int(attrs["start"])),
            )
        )

    def _start_scaninfo(self, attrs):
        """ Create a ScanInfo from a <scaninfo> element. """
        self._events.append(
            ScanInfo(
                attrs["type"],
                attrs["protocol"],
                int(attrs["numservices"]),
                attrs["services"],
            )
        )

    def _start_taskprogress(self, attrs):
        """
        Create a TaskProgress from a <taskprogress> element.
        """
        self._events.append(
            TaskProgress(
                attrs["task"],
                datetime.utcfromtimestamp(int(attrs["time"])),
                float(attrs["percent"]),
            )
        )

    def _start_host(self, attrs):
        """
        Start a Host from a <host> element.
        """
        self._current_host = Host(
            datetime.utcfromtimestamp(int(attrs["starttime"])),
            datetime.utcfromtimestamp(int(attrs["endtime"])),
        )

    def _stop_host(self):
        """ Finish a Host object. """
        self._events.append(self._current_host)
        self._current_host = None

    def _start_status(self, attrs):
        """ Create a Status object from a <status> element. """
        self._current_host.status = Status(attrs["state"], attrs["reason"])

    def _start_address(self, attrs):
        """ Set the host address from an <address> element. """
        addrtype = attrs["addrtype"]
        if addrtype == "ipv4":
            self._current_host.address = IPv4Address(attrs["addr"])
        elif addrtype == "ipv6":
            self._current_host.address = IPv6Address(attrs["addr"])
        else:
            raise NmapXmlParseException(f"Invalid addrtype: {addrtype}")

    def _start_hostname(self, attrs):
        """ Add a hostname from a <hostname> element. """
        self._current_host.hostnames.append(attrs["name"])

    def _start_extraports(self, attrs):
        """ Create an ExtraPorts from an <extraports> element. """
        self._current_host.extraports = ExtraPorts(attrs["state"], int(attrs["count"]))

    def _start_port(self, attrs):
        """ Start a Port object from a <port> element. """
        self._current_port = Port(attrs["protocol"], int(attrs["portid"]),)

    def _stop_port(self):
        """ Finish a Port object. """
        self._current_host.ports.append(self._current_port)
        self._current_port = None

    def _start_state(self, attrs):
        """ Create a PortState object from a <state> element. """
        self._current_port.state = PortState(attrs["state"], attrs["reason"])

    def _start_service(self, attrs):
        """ Set Port.service from a <service> element. """
        self._current_port.service = Service(
            attrs["name"], attrs.get("product"), attrs.get("version")
        )

    def _start_cpe(self, attrs):
        """ Start capturing text from <cpe> element. """
        self.start_text_capture()

    def _stop_cpe(self):
        """ Add captured text from </cpe> to current port's CPE's. """
        cpe = self.stop_text_capture().strip()
        self._current_port.cpes.append(cpe)

    def _start_script(self, attrs):
        """ Start a dictionary containing script data from a <script>. """
        self._current_script_name = attrs["id"]
        self._current_script = {"output": attrs["output"]}

    def _stop_script(self):
        """ Finish a dictionary containing script data from a </script>. """
        # print(f"adding key={self._current_script_name} value={self._current_script}")
        self._current_port.script[self._current_script_name] = self._current_script
        self._current_script = None
        self._current_script_name = None

    def _start_elem(self, attrs):
        """ Start an item for a script dictionary from an <elem>. """
        self._current_script_key = attrs["key"]
        self.start_text_capture()

    def _stop_elem(self):
        """ Finish an item for a script dictionary from an </elem>. """
        value = self.stop_text_capture()
        self._current_script[self._current_script_key] = value
        self._current_script_key = None

    def _start_finished(self, attrs):
        """ Create a Finished object from a <finished> element. """
        self._events.append(
            Finished(
                finished=datetime.utcfromtimestamp(int(attrs["time"])),
                summary=attrs["summary"],
                exit=attrs["exit"],
            )
        )


@dataclass
class NmapRun:
    """ A model for the <nmaprun> element. """

    scanner: str
    scanner_version: str
    command_line: str
    started: datetime


@dataclass
class ScanInfo:
    """ A model for the <scaninfo> element. """

    type_: str
    protocol: str
    numservices: int
    services: str


@dataclass
class TaskProgress:
    """ A model for the <taskprogress> element. """

    task: str
    time: datetime
    percent: float
    remaining: typing.Optional[int] = None
    est_completion: typing.Optional[datetime] = None


@dataclass
class Status:
    """ A model for the <status> element. """

    state: str
    reason: str


@dataclass
class ExtraPorts:
    state: str
    count: int


@dataclass
class Host:
    """ A model for a <host> element. """

    starttime: datetime
    endtime: datetime
    address: typing.Union[IPv4Address, IPv6Address, None] = None
    status: typing.Optional[Status] = None
    service: typing.Optional[str] = None
    hostnames: typing.List[str] = field(default_factory=list)
    ports: typing.List[Port] = field(default_factory=list)
    extraports: typing.Optional[ExtraPorts] = None


@dataclass
class PortState:
    """ A model for a <state> element. """

    state: str
    reason: str


@dataclass
class Service:
    """ A model for a <service> element. """

    name: str
    product: str
    version: str


@dataclass
class Port:
    """ A model for a <port> element. """

    protocol: str
    portid: int
    state: typing.Optional[PortState] = None
    service: typing.Optional[Service] = None
    cpes: typing.List[str] = field(default_factory=list)
    script: typing.Dict[str, typing.Dict[str, str]] = field(default_factory=dict)


@dataclass
class Finished:
    """ A model for a <finished> element. """

    finished: datetime
    summary: str
    exit: str
