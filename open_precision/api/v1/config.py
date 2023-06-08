from fastapi import APIRouter

config_router = APIRouter(
    prefix="/config",
    tags=["config"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@config_router.get("/get")
async def get_config():
    return {"config": "config"}
