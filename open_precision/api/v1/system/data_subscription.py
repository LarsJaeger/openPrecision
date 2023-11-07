from fastapi import APIRouter, Body

from open_precision.api.utils import engine_endpoint

data_subscription_router = APIRouter(
    prefix="/data_subscription",
    tags=["data_subscription"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@data_subscription_router.post("/connect_client")
@engine_endpoint
def connect_data_subscription(hub, sid: str = Body(embed=True)):
    hub.data.inner_on_connect(sid)


@data_subscription_router.post("/disconnect_client")
@engine_endpoint
def disconnect_data_subscription(hub, sid: str = Body(embed=True)):
    hub.data.inner_on_disconnect(sid)


@data_subscription_router.post("/remove_all")
@engine_endpoint
def remove_all_data_subscriptions(hub, sid: str = Body(embed=True)):
    hub.data.remove_all_data_subscriptions(sid)
