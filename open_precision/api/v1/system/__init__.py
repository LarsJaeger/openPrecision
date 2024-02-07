from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.api.v1.system.data_subscription import data_subscription_router
from open_precision.api.v1.system.plugin import plugin_router

if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub

system_router = APIRouter(
	prefix="/system",
	tags=["system"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)
routers = [data_subscription_router, plugin_router]

for router in routers:
	system_router.include_router(router)


@system_router.post("/stop")
@engine_endpoint
def post_stop(hub: SystemHub) -> None:
	hub.stop()


@system_router.post("/start_trace")
@engine_endpoint
def post_start_trace(hub: SystemHub):
	# TODO
	pass


@system_router.post("/stop_trace")
@engine_endpoint
def post_stop_trace(hub: SystemHub):
	# TODO
	pass
