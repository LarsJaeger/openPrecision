from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import GlobalPositioningSystem

gps_router = APIRouter(
    prefix="/gps",
    tags=["gps"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@gps_router.get("/location")
@engine_endpoint
def get_position(hub):
    return hub.plugins[GlobalPositioningSystem].location
