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
from ..nmap.loader import load_scan


logger = logging.getLogger(__name__)


@dispatch.handler
async def upload_scan(base64_data: str) -> dict:
    data = b64decode(base64_data.encode("utf8"))
    scan = await trio.to_thread.run_sync(load_scan, data)
    scan_id = await insert_host_scan(dispatch.ctx.db, scan)
    return {"scan_id": scan_id}


@dispatch.handler
async def list_scans() -> dict:
    return {"scans": await list_host_scans(dispatch.ctx.db)}


@dispatch.handler
async def get_scan(scan_id: str) -> dict:
    return await get_host_scan(dispatch.ctx.db, scan_id)
