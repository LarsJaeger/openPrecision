from __future__ import annotations
from typing import TYPE_CHECKING

from fastapi import APIRouter
from open_precision.core.model.waypoint import Waypoint

from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
	GlobalPositioningSystem,
)
from open_precision.api.utils import engine_endpoint


if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub

loc_store_router = APIRouter(
	prefix="/store",
	tags=["store"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)


@loc_store_router.post("/{obj_type}/{name}")
@engine_endpoint
def post_store_loc(hub: SystemHub, name: str):
	add_to_location_store(hub.plugins[GlobalPositioningSystem].location, name=name)


@loc_store_router.get("/{obj_type}/{name}")
@engine_endpoint
def get_loc_by_name(hub: SystemHub, name: str):
	return Waypoint.get_by_name(name)


@loc_store_router.get("/{obj_type}/")
@engine_endpoint
def get_loc_name_list(hub: SystemHub):
	return get_waypoint_names()


@loc_store_router.delete("/{obj_type}/{name}")
@engine_endpoint
def delete_loc_by_name(hub: SystemHub, name: str):
	delete_from_location_store(name)
