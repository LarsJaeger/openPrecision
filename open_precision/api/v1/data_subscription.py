from typing import TYPE_CHECKING

from fastapi import APIRouter

if TYPE_CHECKING:
    pass

data_subscription_router = APIRouter(
    prefix="/data_subscription",
    tags=["data_subscription"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

"""
@data_subscription_router.post("/subscribe")
async def subscribe(socket_id: str, queue_system_task=Depends(queue_system_task_dependency)):

    def subscribe_inner(hub: SystemHub):
        hub.data.add_data_subscription(sid=socket_id, fn=)
"""
