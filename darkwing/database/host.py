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
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from trio_asyncio import aio_as_trio
import typing

import bson
from motor.motor_asyncio import AsyncIOMotorClient
from pymaybe import maybe
import pymongo

from ..model.page import PageRequest, PageResult


class HostPortTransport(Enum):
    UDP = "UDP"
    TCP = "TCP"


class HostPortState(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    FILTERED = "FILTERED"


@dataclass
class HostPortService:
    name: str
    product: str
    version: str
    method: str
    confidence: float
    cpes: typing.List[str]

    @staticmethod
    def from_db(doc):
        return HostPortService(
            doc["name"],
            doc["product"],
            doc["version"],
            doc["method"],
            doc["confidence"],
            doc["cpes"],
        )


@dataclass
class HostPort:
    number: int
    transport: HostPortTransport
    state: HostPortState
    state_reason: str
    service: HostPortService

    @staticmethod
    def from_db(doc):
        return HostPort(
            doc["number"],
            HostPortTransport(doc["transport"]),
            HostPortState(doc["state"]),
            doc["state_reason"],
            HostPortService.from_db(doc["service"]),
        )


@dataclass
class Host:
    host_id: str
    started: typing.Optional[datetime]
    completed: typing.Optional[datetime]
    state: str
    state_reason: str
    addresses: typing.List[typing.Union[IPv4Address, IPv6Address]]
    hostnames: typing.List[str]
    ports: typing.List[HostPort]

    @staticmethod
    def from_db(doc):
        return Host(
            str(doc["_id"]),
            doc["started"],
            doc["completed"],
            doc["state"],
            doc["state_reason"],
            # TODO IPV6 support
            [IPv4Address(addr) for addr in doc["addresses"]],
            doc["hostnames"],
            [HostPort.from_db(p) for p in doc["ports"]],
        )


@dataclass
class HostListItem:
    host_id: str
    started: typing.Optional[datetime]
    completed: typing.Optional[datetime]
    state: str
    state_reason: str
    addresses: typing.List[typing.Union[IPv4Address, IPv6Address]]
    hostnames: typing.List[str]

    @staticmethod
    def from_db(doc):
        return HostListItem(
            str(doc["_id"]),
            doc["started"],
            doc["completed"],
            doc["state"],
            doc["state_reason"],
            # TODO IPV6 support
            [IPv4Address(addr) for addr in doc["addresses"]],
            doc["hostnames"],
        )


class HostDb:
    @staticmethod
    @aio_as_trio
    async def list_hosts(db: AsyncIOMotorClient, page: PageRequest) -> PageResult:
        """ List hosts. """
        skip = page.page_number * page.items_per_page
        sort_dir = pymongo.ASCENDING if page.sort_ascending else pymongo.DESCENDING
        total = await db.darkwing.host.count_documents({})
        # TODO project the fields we actually use, e.g. no ports
        cursor = db.darkwing.host.find(skip=skip, limit=page.items_per_page)
        hosts: typing.List[HostListItem] = list()
        async for doc in cursor:
            hosts.append(HostListItem.from_db(doc))
        return PageResult(total, hosts)

    @staticmethod
    @aio_as_trio
    async def get_host(db: AsyncIOMotorClient, id_: str) -> dict:
        """ Get a scan document. """
        doc = await db.darkwing.host.find_one({"_id": bson.ObjectId(id_)})
        return Host.from_db(doc)
