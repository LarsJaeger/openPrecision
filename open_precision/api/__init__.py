from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import socketio
import uvicorn
from aioprocessing import AioQueue
from fastapi import FastAPI, APIRouter
from socketio import AsyncServer, AsyncRedisManager
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from open_precision.api.config import config_router

if TYPE_CHECKING:
    pass


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


class API:
    def __init__(self, task_queue: AioQueue):
        # define the socketio server:
        url = 'redis://redis:6379'
        self._socketio_server: AsyncServer = AsyncServer(client_manager=AsyncRedisManager(url),
                                                         async_mode='asgi',
                                                         cors_allowed_origins="*")

        # define socketio events:
        @self._socketio_server.event
        async def connect(sid, environment, auth):
            print('[INFO] client connected with socketid: ', sid)
            self._socketio_server.enter_room(sid, 'target_machine_state')  # TODO make dynamic
            self._socketio_server.enter_room(sid, 'course')
            self._socketio_server.enter_room(sid, 'vehicle_state')

        @self._socketio_server.event
        async def disconnect(sid):
            print('[INFO] client disconnected with socketid: ', sid)
            self._socketio_server.leave_room(sid, 'target_machine_state')
            self._socketio_server.leave_room(sid, 'course')
            self._socketio_server.leave_room(sid, 'vehicle_state')

        # define the fastapi app:
        self.app = FastAPI()

        origins = [
            "*"
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # serve the static frontend
        self.app.mount("/app", StaticFiles(directory="/app/open_precision_frontend", html=True), name="static")
        # self.app.mount("/", StaticFiles(="/app/open_precision_frontend/index.html"), name="static")

        # server the socketio app
        self.app.mount("/sockets", socketio.ASGIApp(self._socketio_server))

        # define the api
        api_router = APIRouter(
            prefix="/api/v1",
            tags=["api", "v1"],
            dependencies=[],
            responses={404: {"description": "Not found"}},
        )
        # include the api routes
        routers = [config_router]

        for router in routers:
            api_router.include_router(router)

        self.app.include_router(api_router)

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", log_level="info")  # , ssl_keyfile="key.pem", ssl_certfile="cert.pem")

    def show_message(self, message: str, message_type: MessageType):
        pass

    def get_input(self, description: str, input_data_type: type) -> any:
        pass
