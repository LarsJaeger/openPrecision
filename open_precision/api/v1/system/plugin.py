from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint

plugin_router = APIRouter(
    prefix="/plugin",
    tags=["plugin"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@plugin_router.get("/enabled")
@engine_endpoint
def get_enabled_plugins(hub):
    return hub.plugins
