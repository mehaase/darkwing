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

import multiprocessing
import os

from motor.motor_asyncio import AsyncIOMotorClient
from trio_asyncio import TrioExecutor


def connect_db(host: str) -> AsyncIOMotorClient:
    _patch_motor()
    return AsyncIOMotorClient(host)


def _patch_motor():
    """ A hack to work around motor incompatibility with trio_asyncio. """
    import motor.frameworks.asyncio

    if "MOTOR_MAX_WORKERS" in os.environ:
        max_workers = int(os.environ["MOTOR_MAX_WORKERS"])
    else:
        max_workers = multiprocessing.cpu_count() * 5

    motor.frameworks.asyncio._EXECUTOR = TrioExecutor()
