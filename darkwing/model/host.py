from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
import typing


class HostState(Enum):
    UP = 0
    DOWN = 1


@dataclass
class Host:
    started: typing.Optional[datetime] = None
    completed: typing.Optional[datetime] = None
    state: typing.Optional[HostState] = None
    state_reason: typing.Optional[str] = None
    addresses: typing.List[typing.Union[IPv4Address, IPv6Address]] = field(
        default_factory=list
    )
    hostnames: typing.List[Hostname] = field(default_factory=list)
    ports: typing.List[Port] = field(default_factory=list)


@dataclass
class Hostname:
    name: str
    type_: typing.Optional[str] = None


class Transport(Enum):
    UDP = 0
    TCP = 1

    @classmethod
    def from_nmap_str(cls, t: str):
        return {"tcp": cls.TCP, "udp": cls.UDP}[t]


class PortState(Enum):
    OPEN = 0
    FILTERED = 1
    CLOSED = 2

    @classmethod
    def from_nmap_str(cls, t: str):
        return {"open": cls.OPEN, "filtered": cls.FILTERED, "closed": cls.CLOSED}[t]


@dataclass
class Service:
    name: str
    product: typing.Optional[str] = None
    version: typing.Optional[str] = None
    method: typing.Optional[str] = None
    confidence: typing.Optional[int] = None
    cpes: typing.List[str] = field(default_factory=list)


@dataclass
class Port:
    number: int
    transport: Transport
    state: typing.Optional[PortState] = None
    state_reason: typing.Optional[str] = None
    service: typing.Optional[Service] = None
