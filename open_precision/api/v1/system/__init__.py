from fastapi import APIRouter

from open_precision.api.v1.system.data_subscription import data_subscription_router
from open_precision.api.v1.system.plugin import plugin_router

system_router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
routers = [data_subscription_router, plugin_router]

for router in routers:
    system_router.include_router(router)
