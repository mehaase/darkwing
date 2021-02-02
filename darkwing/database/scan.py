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
from trio_asyncio import aio_as_trio
import typing

import bson
from motor.motor_asyncio import AsyncIOMotorClient
from pymaybe import maybe

from ..model.host import Port
from ..model.scan import HostScan


@aio_as_trio
async def insert_host_scan(db: AsyncIOMotorClient, scan: HostScan) -> bson.ObjectId:
    """
    Insert a new scan document and new host documents.
    """
    host_docs: typing.List[dict] = list()
    if scan.hosts:
        # TODO batch inserts
        for host in scan.hosts:
            host_docs.append(
                {
                    "started": host.started,
                    "completed": host.completed,
                    "state": maybe(host.state).name.or_else(None),
                    "state_reason": host.state_reason,
                    "addresses": [str(a) for a in host.addresses],
                    "hostnames": list(host.hostnames),
                    "ports": [_port_to_dict(p) for p in host.ports],
                }
            )

        result = await db.darkwing.host.insert_many(host_docs)
        host_ids = result.inserted_ids
    else:
        host_ids = list()

    scan_doc = {
        "scanner": scan.scanner,
        "scanner_version": scan.scanner_version,
        "command_line": scan.command_line,
        "started": scan.started,
        "completed": scan.completed,
        "hosts": host_ids,
    }
    result = await db.darkwing.scan.insert_one(scan_doc)
    scan_id = result.inserted_id
    return str(scan_id)


@aio_as_trio
async def list_host_scans(db: AsyncIOMotorClient) -> list:
    """ List host scan documents. """
    cursor = db.darkwing.scan.find()
    scan_docs: typing.List[dict] = list()
    async for doc in cursor:
        scan_docs.append(
            {
                "scan_id": str(doc["_id"]),
                "scanner": doc["scanner"],
                "scanner_version": doc["scanner_version"],
                "command_line": doc["command_line"],
                "started": maybe(doc["started"]).isoformat().or_else(None),
                "completed": maybe(doc["completed"]).isoformat().or_else(None),
                "host_count": len(doc["hosts"]),
            }
        )
    return scan_docs


@aio_as_trio
async def get_host_scan(db: AsyncIOMotorClient, id_: bson.ObjectId) -> dict:
    """ Get a scan document. """
    doc = await db.darkwing.scan.find_one({"_id": bson.ObjectId(id_)})
    return {
        "scan_id": str(doc["_id"]),
        "scanner": doc["scanner"],
        "scanner_version": doc["scanner_version"],
        "command_line": doc["command_line"],
        "started": maybe(doc["started"]).isoformat().or_else(None),
        "completed": maybe(doc["completed"]).isoformat().or_else(None),
        "host_count": len(doc["hosts"]),
    }


def _port_to_dict(port: Port) -> dict:
    svc = port.service
    return {
        "number": port.number,
        "transport": port.transport.name,
        "state": maybe(port.state).name.or_else(None),
        "state_reason": port.state_reason,
        "service": {
            "name": maybe(svc).name.or_else(None),
            "product": maybe(svc).product.or_else(None),
            "version": maybe(svc).version.or_else(None),
            "method": maybe(svc).method.or_else(None),
            "confidence": maybe(svc).confidence.or_else(None),
            "cpes": list(svc.cpes) if svc else None,
        },
    }
