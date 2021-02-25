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
from copy import copy
from dataclasses import dataclass
import logging
import typing

# from itsdangerous import BadSignature
import trio
from trio_jsonrpc import (
    Dispatch,
    JsonRpcConnection,
    JsonRpcConnectionType,
    JsonRpcException,
)
from trio_jsonrpc.transport.ws import WebSocketTransport
import trio_websocket


if typing.TYPE_CHECKING:
    import configparser
    from motor.motor_asyncio import AsyncIOMotorClient


# Import the server handler modules after dispatch is defined so that they can use the
# object to register handler functions.
dispatch = Dispatch()
import darkwing.server.host
import darkwing.server.scan

logger = logging.getLogger(__name__)


@dataclass
class DispatchContext:
    config: configparser.ConfigParser
    db: AsyncIOMotorClient
    # token_signer: TimedJSONWebSignatureSerializer
    user: typing.Optional[str] = None


# class NotAuthorizedError(JsonRpcApplicationError):
#     ERROR_CODE = -1
#     ERROR_MESSAGE = "The user is not authorized to execute this method."


# def login_required(fn):
#     """ A decorator that makes sure a user is logged in. """

#     @wraps(fn)
#     async def wrapper(*args, **kwargs):
#         if dispatch.ctx.user is None:
#             raise NotAuthorizedError(
#                 f"The user is not authorized to execute this method: {fn.__name__}"
#             )
#         return await fn(*args, **kwargs)

#     return wrapper


# @dispatch.handler
# async def login(username, password):
#     authenticated = await dispatch.ctx.db.login(username, password)
#     if authenticated:
#         dispatch.ctx.user = username
#         token_data = {"username": username}
#         token = dispatch.ctx.token_signer.dumps(token_data).decode("ascii")
#     else:
#         token = None
#     return {
#         "token": token,
#         "authenticated": authenticated,
#     }


# @dispatch.handler
# async def login_token(token):
#     username = None
#     authenticated = False
#     try:
#         token_data = dispatch.ctx.token_signer.loads(token)
#         username = token_data["username"]
#         authenticated = True
#         dispatch.ctx.user = token_data["username"]
#     except BadSignature as bs:
#         dispatch.ctx.user = None
#         logger.error("Failed to validate authentication token: " + str(bs))
#     return {"username": username, "authenticated": authenticated}


# @dispatch.handler
# async def register(username, password, full_name):
#     msg = await dispatch.ctx.db.register(username, password, full_name)
#     if msg is not None:
#         raise RegistrationError(msg)
#     return True


async def run_server(ip, port, base_context, task_status=trio.TASK_STATUS_IGNORED):
    """
    Starts a new WebSocket server on the specified IP/hostname and port.

    SSL is always disabled because this should be run behind a proxy server, and the
    proxy can terminate SSL.
    """

    async def heartbeat(ws, interval):
        """
        Keep a connection open by sending periodic WS pings.
        """
        while True:
            await trio.sleep(interval)
            await ws.ping()

    async def responder(recv_channel, conn):
        """ Gathers results from handlers and sends them back to the client. """
        async for request, result in recv_channel:
            if isinstance(result, JsonRpcException):
                await conn.respond_with_error(request, result.get_error())
            else:
                if result is None:
                    result = {}
                await conn.respond_with_result(request, result)

    async def connection_handler(ws_request):
        """ The handler for each new connection. """
        try:
            # Complete the WebSocket handshake.
            remote_address = ws_request.remote.address
            remote_port = ws_request.remote.port
            logger.info(
                "New connection from %s:%s", remote_address, remote_port,
            )
            ws = await ws_request.accept()

            # Wrap the WebSocket in a JSON-RPC connection.
            transport = WebSocketTransport(ws)
            rpc_conn = JsonRpcConnection(transport, JsonRpcConnectionType.SERVER)
            result_send, result_recv = trio.open_memory_channel(10)

            async with trio.open_nursery() as conn_nursery:
                conn_nursery.start_soon(responder, result_recv, rpc_conn)
                conn_nursery.start_soon(rpc_conn._background_task)
                conn_nursery.start_soon(heartbeat, ws, 30)
                async with dispatch.connection_context(copy(base_context)):
                    # This is the heart of the server: wait for an incoming request and
                    # dispatch it.
                    async for request in rpc_conn.iter_requests():
                        logger.info(
                            "%s:%s [user=%s] %s()",
                            remote_address,
                            remote_port,
                            dispatch.ctx.user,
                            request.method,
                        )
                        conn_nursery.start_soon(
                            dispatch.handle_request, request, result_send
                        )
                # When the serve_requests() returns, it means the server will not
                # receieve any more events, and we can cancel the background tasks.
                logger.info(
                    "Connection closed %s:%s", remote_address, remote_port,
                )
                conn_nursery.cancel_scope.cancel()
        except Exception:
            logger.exception("An unhandled exception crashed a connection handler")

    server = await trio_websocket.serve_websocket(
        connection_handler,
        ip,
        port,
        ssl_context=None,
        task_status=task_status,
        max_message_size=10_485_760,  # 10MB
    )
    task_status.started(server)
