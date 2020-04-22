from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
import typing


from .host import Host


@dataclass
class HostScan:
    scanner: str
    scanner_version: str
    command_line: typing.Optional[str] = None
    started: typing.Optional[datetime] = None
    completed: typing.Optional[datetime] = None
    hosts: typing.List[Host] = field(default_factory=list)
