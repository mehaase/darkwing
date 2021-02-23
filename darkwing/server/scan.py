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
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
import logging
import typing

from lxml import etree
from pymaybe import maybe
import trio

from . import dispatch
from ..database.scan import ScanDb
from ..model.page import PageRequest, PageResult
from ..nmap.loader import load_scan


logger = logging.getLogger(__name__)


@dispatch.handler
async def upload_scan(base64_data: str) -> dict:
    data = b64decode(base64_data.encode("utf8"))
    scan = await trio.to_thread.run_sync(load_scan, data)
    scan_id = await ScanDb.insert_scan(dispatch.ctx.db, scan)
    return {"scan_id": scan_id}


@dispatch.handler
async def list_scans(page: dict) -> dict:
    def jsonify_scan(scan):
        return {
            "scan_id": scan.scan_id,
            "scanner": scan.scanner,
            "scanner_version": scan.scanner_version,
            "command_line": scan.command_line,
            "started": maybe(scan.started).isoformat().or_else(None),
            "completed": maybe(scan.completed).isoformat().or_else(None),
            "host_count": scan.host_count,
        }

    result = await ScanDb.list_scans(dispatch.ctx.db, PageRequest.from_json(page))
    return result.serialize(jsonify_scan)


@dispatch.handler
async def get_scan(scan_id: str) -> dict:
    return await ScanDb.get_scan(dispatch.ctx.db, scan_id)
