from fastapi import APIRouter

system_router = APIRouter(
    prefix="/sensor",
    tags=["sensor"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
routers = []

for router in routers:
    system_router.include_router(router)
