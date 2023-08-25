from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit import InertialMeasurementUnit

imu_router = APIRouter(
    prefix="/imu",
    tags=["imu"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@imu_router.get("/acceleration")
@engine_endpoint
def get_acceleration(hub):
    return hub.plugins[InertialMeasurementUnit].scaled_acceleration


@imu_router.get("/angular_acceleration")
@engine_endpoint
def get_angular_acceleration(hub):
    return hub.plugins[InertialMeasurementUnit].scaled_angular_acceleration


@imu_router.get("/scaled_magnetometer")
@engine_endpoint
def get_scaled_magnetometer(hub):
    return hub.plugins[InertialMeasurementUnit].scaled_magnetometer
