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

import argparse
import logging
import os
import signal
import subprocess
import sys
import time
from threading import Timer

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from . import project_path
from .bootstrap import Bootstrap

reloader_log = logging.getLogger("reloader")


class ProcessWatchdog(FileSystemEventHandler):
    """ Handle watchdog events by restarting a subprocess. """

    def __init__(self):
        """ Constructor. """
        self._process = None
        self._reload_timer = None

    def dispatch(self, event):
        """ Handle filesystem events. """
        path = event.src_path
        file = os.path.basename(path)
        # TODO: rm
        reloader_log.info("File %s: %s", event.event_type, event.src_path)

        if self._file_should_trigger_reload(file):
            reloader_log.info("File %s: %s", event.event_type, event.src_path)
            if self._reload_timer:
                self._reload_timer.cancel()
            self._reload_timer = Timer(1.0, self.reload)
            self._reload_timer.start()

    def _file_should_trigger_reload(self, file):
        """ Return True if this file should trigger a reload. """
        if file.endswith(".py") and not file.startswith("test_"):
            return True
        elif file.endswith(".ini"):
            return True
        return False

    def join(self):
        """ Wait for subprocess to exit. """
        try:
            self._process.wait()
        except AttributeError:
            # Process is None, i.e. already gone.
            pass

    def reload(self):
        """ Shut down the target process and start a new one. """
        self._reload_timer.cancel()
        self._reload_timer = None
        reloader_log.info("Reloading…")
        self.terminate_process()
        self.start_process()

    def start_process(self):
        """ Start the subprocess. """
        if self._process is not None:
            msg = "Cannot start subprocess if it is already running."
            raise RuntimeError(msg)

        time.sleep(1)
        args = [sys.executable, "-m", __package__] + sys.argv[1:]
        new_env = dict(os.environ)
        new_env["WATCHDOG_RUNNING"] = "1"
        self._process = subprocess.Popen(args, env=new_env)

    def terminate_process(self):
        """ Terminate the subprocess. """
        if self._process is not None:
            try:
                self._process.send_signal(signal.SIGINT)
                self._process.wait()
                self._process = None
            except ProcessLookupError:
                pass  # The process already died.


class Reloader:
    """ Reloads the subprocess when a source file is modified. """

    def __init__(self):
        """ Constructor. """
        self._observer = None
        self._running = False
        self._watchdog = None

    def run(self):
        """ Run the reloader. """
        reloader_log.info("Running with reloader...")
        self._watchdog = ProcessWatchdog()
        self._watchdog.start_process()

        self._observer = Observer()
        self._observer.schedule(
            self._watchdog, str(project_path("darkwing")), recursive=True
        )
        self._observer.start()

        try:
            while True:
                self._watchdog.join()
        except KeyboardInterrupt:
            reloader_log.info("Caught SIGINT (shutting down)")
            self.shutdown()

    def shutdown(self):
        """ Exit the reloader. """
        self._watchdog.terminate_process()
        self._observer.stop()
        self._observer.join()


def configure_logging(log_level, log_file):
    """ Set default format and output stream for logging. """
    # Set up console logging
    log_format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"
    log_formatter = logging.Formatter(log_format, log_date_format)
    log_level = getattr(logging, log_level.upper())
    log_handler = logging.StreamHandler(sys.stderr)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(log_level)

    darkwing_logger = logging.getLogger("darkwing")
    darkwing_logger.addHandler(log_handler)
    darkwing_logger.setLevel(log_level)

    reloader_logger = logging.getLogger("reloader")
    reloader_logger.addHandler(log_handler)
    reloader_logger.setLevel(log_level)

    # Set up log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)
    darkwing_logger.addHandler(file_handler)


def get_args():
    """ Parse command line arguments. """
    arg_parser = argparse.ArgumentParser(description="Darkwing")
    arg_parser.add_argument(
        "--log-level",
        default="info",
        metavar="LEVEL",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set logging verbosity (default: info)",
    )
    arg_parser.add_argument(
        "--ip",
        default="127.0.0.1",
        help="The IP address to bind to (default: 127.0.0.1)",
    )
    arg_parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="The TCP port to bind to (default: 8080)",
    )
    arg_parser.add_argument(
        "--reload",
        action="store_true",
        help="Auto-reload when code or config is modified.",
    )
    default_log = project_path("darkwing.log")
    arg_parser.add_argument(
        "--log-file",
        help="Write logs to the specified file (in addition to the console log).",
        default=str(default_log),
    )
    return arg_parser.parse_args()


def main():
    """ Set up watchdog or run Darkwing. """
    args = get_args()
    configure_logging(args.log_level, args.log_file)

    if args.reload and os.getenv("WATCHDOG_RUNNING") is None:
        reloader = Reloader()
        reloader.run()
    else:
        bootstrap = Bootstrap(args)
        bootstrap.run()


if __name__ == "__main__":
    main()
