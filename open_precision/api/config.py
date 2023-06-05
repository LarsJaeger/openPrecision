from fastapi import APIRouter

config_router = APIRouter(
    prefix="/config",
    tags=["config"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
