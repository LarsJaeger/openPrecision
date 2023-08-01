from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.vehicle_state_builder import VehicleStateBuilder

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub

vehicle_state_router = APIRouter(
    prefix="/vehicle_state",
    tags=["vehicle_state"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@vehicle_state_router.get("/")
@engine_endpoint
def _get_vehicle_state(hub):
    return hub.plugins[VehicleStateBuilder].vehicle_state.location
