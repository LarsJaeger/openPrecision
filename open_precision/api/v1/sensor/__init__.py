from fastapi import APIRouter

from open_precision.api.v1.sensor.gps import gps_router
from open_precision.api.v1.sensor.imu import imu_router

sensor_router = APIRouter(
    prefix="/sensor",
    tags=["sensor"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
routers = [gps_router, imu_router]

for router in routers:
    sensor_router.include_router(router)
