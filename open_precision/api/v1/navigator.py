from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.core.plugin_base_classes.vehicle_state_builder import VehicleStateBuilder

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub

navigator_router = APIRouter(
    prefix="/navigator",
    tags=["navigator"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@navigator_router.get("/target_steering_angle")
@engine_endpoint
def _get_target_steering_angle(hub):
    return hub.plugins[Navigator].target_machine_state.steering_angle
