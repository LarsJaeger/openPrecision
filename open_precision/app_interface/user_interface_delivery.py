from __future__ import annotations

import os.path
from enum import Enum
from typing import TYPE_CHECKING

import socketio
import uvicorn
from socketio.asyncio_redis_manager import AsyncRedisManager
from socketio.asyncio_server import AsyncServer

if TYPE_CHECKING:
    from open_precision.manager import Manager


class MessageType(Enum):
    """
    Enum for the different message types.
    """
    INFO = 0
    DEBUG = 1
    WARNING = 2
    SUCCESS = 3
    CRITICAL = 4
    ERROR = 5


class UserInterfaceDelivery:
    def __init__(self, manager: Manager):
        self._manager = manager
        url = 'redis://redis:6379'
        self._server: AsyncServer = AsyncServer(client_manager=AsyncRedisManager(url),
                                                async_mode='asgi',
                                                cors_allowed_origins="*")

        # serve static files
        base_dir = os.path.dirname(__file__)
        static_files = {
            '/': os.path.join(base_dir, os.path.relpath("static/index.html")),
            '/favicon.ico': os.path.join(base_dir, os.path.relpath("static/favicon.ico")),
            '/app': os.path.join(base_dir, os.path.relpath("static/index.html")),
            '/static': os.path.join(base_dir, os.path.relpath("static"))
        }

        @self._server.event
        async def connect(sid, environment, auth):
            print('[INFO] client connected with socketid: ', sid)
            self._server.enter_room(sid, 'target_machine_state')  # TODO make dynamic

        @self._server.event
        async def disconnect(sid):
            print('[INFO] client disconnected with socketid: ', sid)
            self._server.leave_room(sid, 'target_machine_state')

        self._app = socketio.ASGIApp(self._server, static_files=static_files)

    def run(self):
        uvicorn.run(self._app, host="0.0.0.0", log_level="info")  # , ssl_keyfile="key.pem", ssl_certfile="cert.pem")

    def show_message(self, message: str, message_type: MessageType):
        pass

    def get_input(self, description: str, input_data_type: type) -> any:
        pass
