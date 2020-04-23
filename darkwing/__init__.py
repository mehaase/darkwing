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

from functools import wraps
import pathlib
import trio
import typing


# We use pathlib to resolve the project root because its synchronous and we can run it
# before we start Trio. Otherwise we'd only be able to resolve paths (and configuration)
# *after* starting Trio.
project_root = trio.Path(pathlib.Path(__file__).resolve().parent.parent)


def project_path(relpath):
    """ Get absolute path to a project-relative path. """
    return project_root / relpath


def async_in_thread(fn):
    """
    This decorator converts a sync function into an async function that runs in a
    thread pool.
    """

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        return await trio.to_thread.run_sync(fn, *args, **kwargs)

    return wrapper


class AppConfig:
    """
    Contains some configuration that is loaded from environment variables.

    Most of the application configuration is stored in the database and exposed through
    the JSON-RPC interface. But some aspects of configuration cannot or should not be
    stored in the database, such as the connection information for the database itself.

    That type of configuration is exposed through environment variables and then
    """

    def __init__(self):
        self.mongo_host = None

    @classmethod
    def from_env(cls, env: typing.Mapping[str, str]):
        config = cls()
        config.mongo_host = env["DARKWING_MONGO_HOST"]
        return config
