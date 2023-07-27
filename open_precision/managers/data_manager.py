from __future__ import annotations

from json import JSONEncoder
from typing import TYPE_CHECKING, Dict, Callable, Any, List

from socketio.asyncio_server import AsyncServer

from open_precision.core.model import DataModelBase

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
        self._data_update_mapping: Dict[Callable[[], Any], List[str]] = {}
        self._connected_clients: list[str] = []

    async def _on_connect(self, sid, environ):
        """
        This function is called by the socketio server when a new client connects. It is not intended to be called from
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
        This function is called by the SystemHub to trigger a data update. It is not intended to be called from outside
        the system update loop.
        :return: None
        """
        data_update_mem = {k: None for k in self._data_update_mapping.keys()}

        # send current states to the user interface if changes occurred
        for fn, subscribers in self._data_update_mapping.items():
            try:
                exec_result = fn()
            except Exception as e:
                exec_result = e

            if data_update_mem[fn] != exec_result:
                for subscriber in subscribers:
                    serialized_result = exec_result.to_json() if isinstance(exec_result, DataModelBase) \
                        else JSONEncoder().encode(exec_result)

                    await self._sio.emit(serialized_result,
                                         to=subscriber)

    async def add_data_subscription(self, sid: str, fn: Callable[[], Any], period_ms: int = 0):
        subscribers = self._data_update_mapping[fn]
        if sid not in subscribers:
            subscribers.append(sid)

    async def remove_data_subscription(self, sid: str, fn: Callable[[], Any]):
        subscribers = self._data_update_mapping[fn]
        if sid in subscribers:
            subscribers.remove(sid)
