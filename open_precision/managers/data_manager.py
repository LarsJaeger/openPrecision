from __future__ import annotations

import traceback
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Any, List, Tuple

from socketio import AsyncRedisManager
from socketio.asyncio_server import AsyncServer

from open_precision.core.model import DataModelBase, CustomJSONEncoder
from open_precision.core.model.data_subscription import DataSubscription

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class DataManager:
    """
    The DataManager manages data subscriptions and data updates. The goal is to bundle periodic api calls to reduce
    computational expenses and network traffic, as well as to move data update work to the server side. These periodic
    tasks either check for new data or are otherwise required to be called periodically.

    Concretely, equivalent system tasks are grouped, then called once if required by the schedule, then multicasted to
    the specified clients via socketio. This is done by the open_precision.api.utils.engine_endpoint decorator, which
    also contains more documentation on how data subscriptions work.
    """

    def __init__(self, manager: SystemHub):
        self.endpoint_dict = None
        self._hub = manager
        url = 'redis://redis:6379'
        self._sio = AsyncServer(client_manager=AsyncRedisManager(url),
                                async_mode='asgi',
                                cors_allowed_origins="*")
        self._sio.on('connect', self._on_connect)
        self._sio.on('socket_id', self._get_socket_id)
        self._data_update_mapping: Dict[DataSubscription, List[str]] = {}  # subscription: [subscribed_sids]
        self._data_update_mem: Dict[
            DataSubscription, Tuple[Any, datetime | None]] = {}  # subscription: (value, last_updated)
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

    async def _get_socket_id(self, sid, data):
        await self._sio.emit("socket_id", data=sid, to=sid)

    async def _on_disconnect(self, sid):
        self._connected_clients.remove(sid)
        for key, subscribers_list in self._data_update_mapping.items():
            if sid in subscribers_list:
                print(f"removed {sid} from subscribers list")
                subscribers_list.remove(sid)
                if len(subscribers_list) == 0:
                    del self._data_update_mapping[key]
        print('disconnect ', sid)

    async def do_update(self):
        """
        This func is called by the SystemHub to trigger a data update. It is not intended to be called from outside
        the system update loop. It recomputes out of date data subscriptions and sends an update to subscribers if the
        value has changed.
        :return: None
        """
        # add subscription to out_of_date list if period length has passed
        out_of_date = []
        now = datetime.now()
        for subscription, (val, time) in self._data_update_mem.items():
            if (time is None) or (((now - time).total_seconds() * 1000) >= subscription.period_length):
                out_of_date.append(subscription)

        # if out of date and value changed: send current states to the user interface
        for subscription in out_of_date:

            current_mem_val, current_mem_time = self._data_update_mem[subscription]
            try:
                exec_result = subscription.func(self._hub, *subscription.args,
                                                **{x: y for (x, y) in subscription.kw_args})
            except Exception as e:
                exec_result = {"exception": traceback.format_exc()}
                if current_mem_time is None or current_mem_val != exec_result:
                    print(f"exception in data subscription {str(hash(subscription))} : \n {traceback.format_exc()}")

            if current_mem_time is None or current_mem_val != exec_result:

                self._data_update_mem[subscription] = (exec_result, datetime.now())
                for subscriber in self._data_update_mapping[subscription]:
                    if isinstance(exec_result, DataModelBase):
                        serialized_result = exec_result.to_json()
                    elif isinstance(exec_result, str):
                        serialized_result = exec_result
                    else:
                        serialized_result = CustomJSONEncoder().encode(exec_result)

                    await self._sio.emit(str(hash(subscription)), data=serialized_result,
                                         to=subscriber)

    async def emit_error(self, e: Exception):
        """
        emit an error in the error room
        """
        await self._sio.emit('error', str(e),
                             room='error')

    def add_data_subscription(self, sid: str, data_subscription: DataSubscription):
        """
        subscribe a socket id to a data subscription
        :param sid:
        :param data_subscription:
        :return:
        """
        if data_subscription in self._data_update_mapping.keys():
            subscribers = self._data_update_mapping[data_subscription]
        else:
            subscribers = []
            self._data_update_mapping[data_subscription] = subscribers
            self._data_update_mem[data_subscription] = (None, None)
        if sid not in subscribers:
            print(f"{sid} subscribed to {str(data_subscription.func)}")
            subscribers.append(sid)

    def remove_data_subscription(self, sid: str, data_subscription: DataSubscription):
        """
        remove a data subscription for a given socket id and data subscription
        :param sid:
        :param data_subscription:
        :return:
        """
        subscribers = self._data_update_mapping[data_subscription]
        if sid in subscribers:
            subscribers.remove(sid)
            print(f"{sid} unsubscribed from {str(data_subscription.func)}")
        if len(subscribers) == 0:
            del self._data_update_mapping[data_subscription]
            del self._data_update_mem[data_subscription]

    def remove_all_data_subscriptions(self, sid: str):
        """
        remove all data subscriptions for a given socket id
        :param sid:
        :return:
        """
        for data_subscription in self._data_update_mapping.keys():
            self.remove_data_subscription(sid, data_subscription)
