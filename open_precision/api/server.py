# define the socketio server:

import socketio
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute
from socketio import AsyncServer, AsyncRedisManager
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from open_precision.api.v1 import v1_router
from open_precision.api.v1.data_subscription import data_subscription_router

url = 'redis://redis:6379'
_socketio_server: AsyncServer = AsyncServer(client_manager=AsyncRedisManager(url),
                                            async_mode='asgi',
                                            cors_allowed_origins="*")


# define socketio events:
@_socketio_server.event
async def connect(sid, environment, auth):
    print('[INFO] client connected with socketid: ', sid)
    _socketio_server.enter_room(sid, 'target_machine_state')  # TODO make dynamic
    _socketio_server.enter_room(sid, 'course')
    _socketio_server.enter_room(sid, 'vehicle_state')


@_socketio_server.event
async def disconnect(sid):
    print('[INFO] client disconnected with socketid: ', sid)
    _socketio_server.leave_room(sid, 'target_machine_state')
    _socketio_server.leave_room(sid, 'course')
    _socketio_server.leave_room(sid, 'vehicle_state')


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
app.include_router(data_subscription_router)
