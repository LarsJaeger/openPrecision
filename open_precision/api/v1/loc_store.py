from __future__ import annotations
from typing import TYPE_CHECKING

from fastapi import APIRouter
from pydantic import BaseModel
from open_precision.core.model.location import Location
from open_precision.core.model.waypoint import Waypoint

from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
	GlobalPositioningSystem,
)
from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.vehicle_state_builder import (
	VehicleStateBuilder,
)


if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub


store_router = APIRouter(
	prefix="/store",
	tags=["store"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)


@store_router.post("/waypoint")
@engine_endpoint
def post_waypoint(hub: SystemHub, name: str, use_raw_location: bool = False):
	loc: Location = None
	if use_raw_location:
		loc = hub.plugins[GlobalPositioningSystem].location
	else:
		loc = hub.plugins[VehicleStateBuilder].current_position.location
	Waypoint(location=loc).store(name)


@store_router.get("/waypoint")
@engine_endpoint
def get_waypoint_by_name(hub: SystemHub, name: str):
	return Waypoint.get(name)


@store_router.get("/waypoint/all")
@engine_endpoint
def get_waypoint_names(hub: SystemHub):
	return Waypoint.get_names()


@store_router.delete("/waypoint")
@engine_endpoint
def unstore_waypoint(hub: SystemHub, name: str):
	Waypoint.unstore(name)
