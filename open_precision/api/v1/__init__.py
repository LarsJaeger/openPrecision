from fastapi import APIRouter

from open_precision.api.v1.config import config_router
from open_precision.api.v1.navigator import navigator_router
from open_precision.api.v1.sensor import sensor_router
from open_precision.api.v1.system import system_router
from open_precision.api.v1.vehicle_state import vehicle_state_router

v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
# include the api routes
routers = [config_router, navigator_router, vehicle_state_router, sensor_router, system_router]
for router in routers:
    v1_router.include_router(router)
