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

from base64 import b64decode
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
import logging
import typing

import bson
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient
from pymaybe import maybe
import trio
from trio_asyncio import aio_as_trio

from . import dispatch
from ..database.host import HostDb
from ..model.page import PageRequest


logger = logging.getLogger(__name__)


@dispatch.handler
async def list_hosts(page: dict) -> dict:
    def jsonify_host_item(host):
        return {
            "host_id": host.host_id,
            "started": maybe(host.started).isoformat().or_else(None),
            "completed": maybe(host.completed).isoformat().or_else(None),
            "state": host.state,
            "state_reason": host.state_reason,
            "addresses": [str(addr) for addr in host.addresses],
            "hostnames": host.hostnames,
            "cover_image": None,
        }

    result = await HostDb.list_hosts(dispatch.ctx.db, PageRequest.from_json(page))
    return result.serialize(jsonify_host_item)


@dispatch.handler
async def get_host(host_id: str) -> dict:
    def jsonify_host(host):
        return {
            "host_id": host.host_id,
            "started": maybe(host.started).isoformat().or_else(None),
            "completed": maybe(host.completed).isoformat().or_else(None),
            "state": host.state,
            "state_reason": host.state_reason,
            "addresses": [str(addr) for addr in host.addresses],
            "hostnames": host.hostnames,
            "cover_image": None,
            "ports": [jsonify_port(p) for p in host.ports],
        }

    def jsonify_port(port):
        return {
            "number": port.number,
            "transport": port.transport.name,
            "state": port.state.name,
            "state_reason": port.state_reason,
            "service": jsonify_service(port.service),
        }

    def jsonify_service(service):
        return {
            "name": service.name,
            "product": service.product,
            "version": service.version,
            "method": service.method,
            "confidence": service.confidence,
            "cpes": service.cpes,
        }

    host = await HostDb.get_host(dispatch.ctx.db, host_id)
    return jsonify_host(host)
