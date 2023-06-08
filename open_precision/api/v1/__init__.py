from fastapi import APIRouter

from open_precision.api.v1.config import config_router
from open_precision.api.v1.course import course_router

v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
# include the api routes
routers = [config_router, course_router]
for router in routers:
    v1_router.include_router(router)
