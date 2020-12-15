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
