# define the socketio server:
from __future__ import annotations

from typing import TYPE_CHECKING

import socketio
from fastapi import FastAPI, APIRouter
from socketio import AsyncServer, AsyncRedisManager
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from open_precision.api.v1 import v1_router

if TYPE_CHECKING:
    pass


def make_app(hub):
    url = 'redis://redis:6379'
    _socketio_server: AsyncServer = AsyncServer(client_manager=AsyncRedisManager(url),
                                                async_mode='asgi',
                                                cors_allowed_origins="*")

    # define socketio events:
    @_socketio_server.event
    async def connect(sid, environment, auth):
        print('[INFO] client connected with socketid: ', sid)

    @_socketio_server.event
    async def disconnect(sid):
        hub.system_task_manager.queue_system_task(hub.data.remove_all_data_subscriptions, sid)
        print('[INFO] client disconnected with socketid: ', sid)

    # define the fastapi app:
    app = FastAPI()

    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # serve the static frontend
    app.mount("/app", StaticFiles(directory="/app/open_precision_frontend", html=True), name="static")

    root_router = APIRouter(
        prefix="",
        tags=["root"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )

    @root_router.get("/")
    async def root():
        """
        Redirects to the frontend
        :return: RedirectResponse
        """
        return RedirectResponse(url='/app')

    # app.mount("/", StaticFiles(="/app/open_precision_frontend/index.html"), name="static")

    # server the socketio app
    app.mount("/sockets", socketio.ASGIApp(_socketio_server))

    # define the api
    api_router = APIRouter(
        prefix="/api",
        tags=["api"],
        dependencies=[],
        responses={404: {"description": "Not found"}},
    )
    api_router.include_router(v1_router)

    app.include_router(api_router)
    app.include_router(root_router)
    return app
