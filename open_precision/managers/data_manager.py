from __future__ import annotations

from datetime import datetime
from json import JSONEncoder
from typing import TYPE_CHECKING, Dict, Callable, Any, List, Tuple

from socketio.asyncio_server import AsyncServer

from open_precision.core.model import DataModelBase
from open_precision.core.model.data_subscription import DataSubscription

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class DataManager:
    """
    The DataManager manages data subscriptions and data updates. The goal is to bundle periodic api calls to reduce
    computational expenses and network traffic, as well as to move data update work to the server side. These periodic
    tasks either check for new data or are otherwise required to be called periodically.

    Concretely, equivalent system tasks are grouped, then called once if required by the schedule, then multicasted to
    the specified clients via socketio. For specific usage, see the documentation of #TODO
    """

    def __init__(self, manager: SystemHub):
        self.endpoint_dict = None
        self._manager = manager
        self._sio = AsyncServer(async_mode='asgi',
                                cors_allowed_origins="*")
        self._sio.on('connect', self._on_connect)
        self._data_update_mapping: Dict[DataSubscription, List[str]] = {}  # subscription: [subscribed_sids]
        self._data_update_mem: Dict[DataSubscription, Tuple[Any, datetime]] = {}  # subscription: (value, last_updated_unix)
        self._connected_clients: list[str] = []

    async def _on_connect(self, sid, environ):
        """
        This func is called by the socketio server when a new client connects. It is not intended to be called from
        outside the system update loop.
        :param sid:
        :param environ:
        :return:
        """
        self._connected_clients.append(sid)
        # TODO auth
        print('connect ', sid)

    async def _on_disconnect(self, sid):
        self._connected_clients.remove(sid)
        print('disconnect ', sid)

    async def do_update(self):
        """
        This func is called by the SystemHub to trigger a data update. It is not intended to be called from outside
        the system update loop. It recomputes out of date data subscriptions and sends an update to subscribers if the
        value has changed.
        :return: None
        """
        data_update_mem = {k: (None, None) for k in self._data_update_mapping.keys()}

        # add subscription to out_of_date list if period length has passed
        out_of_date = []
        now = datetime.now()
        for subscription, (val, time) in data_update_mem:
            if now - time >= subscription.period_length:
                out_of_date.append(subscription)

        # if out of date and value changed: send current states to the user interface
        for subscription in out_of_date:
            try:
                exec_result = subscription.func(*subscription.args, **{x: y for (x, y) in subscription.kw_args})
            except Exception as e:
                exec_result = e

            if data_update_mem[subscription][0] != exec_result:
                for subscriber in self._data_update_mapping[subscription]:
                    serialized_result = exec_result.to_json() if isinstance(exec_result, DataModelBase) \
                        else JSONEncoder().encode(exec_result)

                    await self._sio.emit(hash(subscription), data=serialized_result,
                                         to=subscriber)

    async def emit_error(self, e: Exception):
        """
        emit an error in the error room
        """
        await self._sio.emit('error', str(e),
                             room='error')

    async def add_data_subscription(self, sid: str, data_subscription: DataSubscription):
        subscribers = self._data_update_mapping[data_subscription]
        if sid not in subscribers:
            subscribers.append(sid)

    async def remove_data_subscription(self, sid: str, data_subscription: DataSubscription):
        subscribers = self._data_update_mapping[data_subscription]
        if sid in subscribers:
            subscribers.remove(sid)
