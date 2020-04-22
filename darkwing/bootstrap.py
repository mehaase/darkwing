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
from dataclasses import dataclass
import logging
import signal
import typing

# from itsdangerous import TimedJSONWebSignatureSerializer
import trio

from . import project_path

# from .database import Database
from .server import DispatchContext, run_server


if typing.TYPE_CHECKING:
    import configparser


logger = logging.getLogger(__name__)


class TerminateSignal(Exception):
    pass


class Bootstrap:
    """ Main class for bootstrapping the application. """

    def __init__(self, config, args):
        """
        Constructor.

        :param config: Output of config parser.
        :param args: Output of argparse.
        """
        self._args = args
        self._config = config

    def run(self):
        """ Run the main task on the event loop. """
        logger.info("Darkwing is starting...")
        try:
            trio.run(self._main, restrict_keyboard_interrupt_to_checkpoints=True)
        except KeyboardInterrupt:
            logger.warning("Received SIGINT: quitting")
        except TerminateSignal:
            logger.warning("Received SIGTERM: quitting")
        logger.info("Darkwing has stopped.")

    async def _main(self):
        """
        The main task.

        :returns: This function runs until cancelled.
        """
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self._sigterm_receiver)

            # Set up database.
            # data_dir = project_path("data")
            # db_file = data_dir / self._config["database"]["name"]
            # db = Database(db_file)

            # Configuration for signed authentication tokens.
            # token_signer = TimedJSONWebSignatureSerializer(
            #     self._config["authentication"]["token_signing_key"],
            #     expires_in=int(self._config["authentication"]["token_expiration"]),
            # )

            # Set up server.
            context = DispatchContext(config=self._config)
            server = await nursery.start(
                run_server, self._args.ip, self._args.port, context
            )
            logger.info(
                "The server is listening on ws://%s:%d/ws/", self._args.ip, server.port,
            )

    async def _sigterm_receiver(self):
        with trio.open_signal_receiver(signal.SIGTERM) as signal_aiter:
            async for _ in signal_aiter:
                raise TerminateSignal()
