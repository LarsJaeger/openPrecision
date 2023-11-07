from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.vehicle_state_builder import (
    VehicleStateBuilder,
)

if TYPE_CHECKING:
    pass

vehicle_state_router = APIRouter(
    prefix="/vehicle_state",
    tags=["vehicle_state"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@vehicle_state_router.get("/")
@engine_endpoint
def get_vehicle_state(hub, ignore_uuid: bool = False):
    ret = hub.plugins[VehicleStateBuilder].vehicle_state
    if ignore_uuid:
        return ret.to_json(field_key_filter=lambda x: x != "uuid")
    else:
        return ret.to_json()


@vehicle_state_router.get("/steering_angle")
@engine_endpoint
def get_steering_angle(hub) -> float:
    return hub.plugins[VehicleStateBuilder].vehicle_state.steering_angle


@vehicle_state_router.get("/speed")
@engine_endpoint
def get_speed(hub) -> float:
    return hub.plugins[VehicleStateBuilder].vehicle_state.speed


@vehicle_state_router.get("/position")
@engine_endpoint
def get_position(hub):
    a = hub.plugins[VehicleStateBuilder].vehicle_state.position
    return a
