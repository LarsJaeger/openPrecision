from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from open_precision.api.dependencies import queue_system_task_dependency
from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub

data_subscription_router = APIRouter(
    prefix="/data_subscription",
    tags=["data_subscription"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@data_subscription_router.post("/subscribe")
async def subscribe(request: Request, queue_system_task=Depends(queue_system_task_dependency)):

    def subscribe_inner(hub: SystemHub):
        hub.data.add_data_subscription()
