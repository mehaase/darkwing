# Darkwing: Your pen test sidekick!
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

import bson
from lxml import etree
from pymaybe import maybe
import trio
from trio_asyncio import aio_as_trio

from . import dispatch

if typing.TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorClient


logger = logging.getLogger(__name__)


@dispatch.handler
async def list_hosts() -> dict:
    return {"hosts": await _db_list_hosts(dispatch.ctx.db)}


@aio_as_trio
async def _db_list_hosts(db: AsyncIOMotorClient) -> list:
    """ List host scan documents. """
    # TODO projection/aggregation to count ports?
    cursor = db.foo_project.host.find()
    host_docs: typing.List[dict] = list()
    async for doc in cursor:
        host_docs.append(
            {
                "host_id": str(doc["_id"]),
                "started": maybe(doc["started"]).isoformat().or_else(None),
                "completed": maybe(doc["completed"]).isoformat().or_else(None),
                "state": doc["state"],
                "state_reason": doc["state_reason"],
                "addresses": doc["addresses"],
                "hostnames": [h["name"] for h in doc["hostnames"]],
                "port_count": len(doc["ports"]),
            }
        )
    return host_docs


@dispatch.handler
async def get_host(host_id: str) -> dict:
    return await _db_get_host(dispatch.ctx.db, host_id)


@aio_as_trio
async def _db_get_host(db: AsyncIOMotorClient, host_id: str) -> list:
    """ List host scan documents. """
    doc = await db.foo_project.host.find_one({"_id": bson.ObjectId(host_id)})
    return {
        "host_id": str(doc["_id"]),
        "started": maybe(doc["started"]).isoformat().or_else(None),
        "completed": maybe(doc["completed"]).isoformat().or_else(None),
        "state": doc["state"],
        "state_reason": doc["state_reason"],
        "addresses": doc["addresses"],
        "hostnames": [{"name": h["name"], "type": h["type"]} for h in doc["hostnames"]],
        "port_count": len(doc["ports"]),
    }
