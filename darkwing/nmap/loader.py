import typing

from ..model.host import Host, HostState, Port, PortState, Service, Transport
from ..model.scan import HostScan
from .parser import (
    Finished as NmapFinished,
    Host as NmapHost,
    NmapXmlParser,
    NmapRun,
    Port as NmapPort,
)


def load_scan(data: str) -> HostScan:
    parser = NmapXmlParser()
    parser.feed(data)
    scan: typing.Optional[HostScan] = None
    for event in parser.events():
        if isinstance(event, NmapRun):
            scan = HostScan(event.scanner, event.scanner_version)
            scan.command_line = event.command_line
            scan.started = event.started
        elif scan and isinstance(event, NmapFinished):
            scan.completed = event.finished
        elif scan and isinstance(event, NmapHost):
            host = Host()
            host.started = event.starttime
            host.completed = event.endtime
            if event.status:
                host.state = _convert_host_state(event.status.state)
                host.state_reason = event.status.reason
            else:
                raise Exception("Nmap is missing host state")
            if event.address:
                host.addresses.append(event.address)
            host.hostnames = list(event.hostnames)
            host.ports = [_convert_port(p) for p in event.ports]
            scan.hosts.append(host)

    if scan is None:
        # TODO clean up
        raise Exception("Failed to load scan")
    else:
        return scan


def _convert_host_state(state: str) -> HostState:
    """
    Convert Nmap host state to host state enum.
    """
    try:
        return {"up": HostState.UP, "down": HostState.DOWN}[state]
    except KeyError:
        raise Exception(f'Invalid nmap host state: "state"')


def _convert_port(nmap_port: NmapPort) -> Port:
    port = Port(nmap_port.portid, _convert_transport(nmap_port.protocol))
    if nmap_port.state:
        port.state = _convert_port_state(nmap_port.state.state)
        port.state_reason = nmap_port.state.reason
    if nmap_port.service:
        service = Service(nmap_port.service.name)
        service.product = nmap_port.service.product
        service.version = nmap_port.service.version
        port.service = service

    return port


def _convert_transport(transport: str) -> Transport:
    try:
        return {"tcp": Transport.TCP, "udp": Transport.UDP,}[transport]
    except KeyError:
        raise Exception(f'Invalid Nmap transport: "{transport}"')


def _convert_port_state(state: str) -> PortState:
    try:
        return {
            "open": PortState.OPEN,
            "closed": PortState.CLOSED,
            "filtered": PortState.FILTERED,
        }[state]
    except KeyError:
        raise Exception(f"Invalid Nmap port state: {state}")

