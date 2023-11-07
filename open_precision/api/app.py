# define the socketio server:
from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import socketio
from fastapi import FastAPI, APIRouter
from socketio import AsyncServer, AsyncRedisManager
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from libraries.starlette.staticfiles import StaticFiles
from open_precision.api.v1 import v1_router

if TYPE_CHECKING:
	pass

url = "redis://redis:6379"

# define the fastapi app:
app = FastAPI()

origins = ["*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# serve the static frontend
try:
	app.mount(
		"/app",
		StaticFiles(directory="/app/open_precision_frontend", html=True),
		name="static",
	)
except RuntimeError:
	print(
		"[ERROR]: Could not mount static files /app/open_precision_frontend make sure to move the built frontend to "
		"the according directory. If this error occurs while building docs, ignore it."
	)

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
	return RedirectResponse(url="/app")


# app.mount("/", StaticFiles(="/app/open_precision_frontend/index.html"), name="static")


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
_socketio_server: AsyncServer = AsyncServer(
	client_manager=AsyncRedisManager(url), async_mode="asgi", cors_allowed_origins="*"
)

# define socketio events:
origin_url: str | None = None


@_socketio_server.event
async def connect(sid, environment):
	"""
	This func is called by the socketio server when a new client connects.
	It will trigger an endpoint to trigger the corresponding inner function in the update loop.
	This complex workaround is necessary, because the socketio server is not part of the fastapi app (it is just mounted
	to the path), so it cannot access the FastAPI's dependency to the system task queue function to trigger logic within
	the update loop.

	:param sid: socket id
	:param environment: environment dict
	:return:
	"""

	global origin_url
	origin_url = environment["HTTP_ORIGIN"]
	endpoint_url = origin_url + "/api/v1/system/data_subscription/connect_client"
	# perform api request with httpx
	async with httpx.AsyncClient() as client:
		response = await client.post(endpoint_url, json={"sid": sid}, timeout=30.0)
	if response.status_code != 200:
		print("[ERROR] could not connect data subscription with socketid: ", sid)
		return

	print("[INFO] client connected with socketid: ", sid)


@_socketio_server.event
async def disconnect(sid):
	"""
	This func is called by the socketio server when a client disconnects.
	It will trigger an endpoint to trigger the corresponding inner function in the update loop.
	This complex workaround is necessary, because the socketio server is not part of the fastapi app (it is just mounted
	to the path), so it cannot access the FastAPI's dependency to the system task queue function to trigger logic within
	the update loop.

	:param sid: socket id
	:return:
	"""
	global origin_url
	if origin_url is None:
		print(
			"[ERROR] origin_url is unknown, could not disconnect data subscription with socketid: ",
			sid,
		)
		return
	endpoint_url = origin_url + "/api/v1/system/data_subscription/disconnect_client"
	# perform api request with httpx
	async with httpx.AsyncClient() as client:
		response = await client.post(endpoint_url, json={"sid": sid})
	if response.status_code != 200:
		print("[ERROR] could not disconnect data subscription with socketid: ", sid)
		return
	print("[INFO] client disconnected with socketid: ", sid)


# server the socketio app
app.mount("/sockets", socketio.ASGIApp(_socketio_server))
