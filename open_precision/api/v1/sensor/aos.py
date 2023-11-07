from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)

aos_router = APIRouter(
    prefix="/aos",
    tags=["aos"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@aos_router.get("/orientation")
@engine_endpoint
def get_orientation(hub):
    return hub.plugins[AbsoluteOrientationSensor].orientation


@aos_router.post("/calibrate")
@engine_endpoint
def calibrate(hub):
    hub.plugins[AbsoluteOrientationSensor].calibrate()
