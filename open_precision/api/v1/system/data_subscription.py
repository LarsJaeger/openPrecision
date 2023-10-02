from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint

data_subscription_router = APIRouter(
    prefix="/data_subscription",
    tags=["data_subscription"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@data_subscription_router.post("/remove_all")
@engine_endpoint
async def remove_all_data_subscriptions(hub, sid: str):
    await hub.data.remove_all_data_subscriptions(sid)
