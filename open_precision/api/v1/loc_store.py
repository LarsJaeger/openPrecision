from __future__ import annotations
from typing import TYPE_CHECKING

from fastapi import APIRouter

from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
	GlobalPositioningSystem,
)
from open_precision.api.utils import engine_endpoint
from open_precision.location_store import (
	add_to_location_store,
	get_location,
	get_location_names,
	delete_from_location_store,
)


if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub

loc_store_router = APIRouter(
	prefix="/loc_store",
	tags=["loc_store"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)


@loc_store_router.post("/{name}")
@engine_endpoint
def post_store_loc(hub: SystemHub, name: str):
	add_to_location_store(hub.plugins[GlobalPositioningSystem].location, name=name)


@loc_store_router.get("/{name}")
@engine_endpoint
def get_loc_by_name(hub: SystemHub, name: str):
	return get_location(name)


@loc_store_router.get("/")
@engine_endpoint
def get_loc_name_list(hub: SystemHub):
	return get_location_names()


@loc_store_router.delete("/{name}")
@engine_endpoint
def delete_loc_by_name(hub: SystemHub, name: str):
	delete_from_location_store(name)
