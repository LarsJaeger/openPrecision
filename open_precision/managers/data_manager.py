from __future__ import annotations

from json import JSONEncoder
from typing import TYPE_CHECKING, Dict, Callable, Any, List

from fastapi.routing import APIRoute
from socketio.asyncio_server import AsyncServer

from open_precision.core.model import DataModelBase

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class DataManager:
    def __init__(self, manager: SystemHub):
        self.endpoint_dict = None
        self._signal_stop = False
        self._manager = manager
        self._sio = None
        self._data_update_mapping: Dict[Callable[[], Any], List[str]] = {}
        self._connected_clients: list[str] = []

    async def _on_connect(self, sid, environ):
        self._connected_clients.append(sid)
        # TODO auth
        print('connect ', sid)

    async def _on_disconnect(self, sid):
        self._connected_clients.remove(sid)
        print('disconnect ', sid)

    async def start_update_loop(self):
        # url = 'redis://redis:6379' TODO evaluate if required
        self._sio = AsyncServer(  # client_manager=AsyncRedisManager(url),
            async_mode='asgi',
            cors_allowed_origins="*")
        await self._sio.on('connect', self._on_connect)
        
        # get endpoints for later subscriptions
        route_list = [x for x in self._manager.api.app.routes if isinstance(x, APIRoute)]
        self.endpoint_dict: dict = {route: route.endpoint for route in route_list}
        
        
        while not self._signal_stop:
            await self.update()
            # await asyncio.sleep(10) # slow down update loop artificially

    async def update(self):
        try:
            # handle actions and deliver responses
            await self._manager.system_task_manager.handle_tasks(amount=10)
        except Exception as e:
            await self._sio.emit('error', str(e),
                                 room='error')
        data_update_mem = {k: None for k in self._data_update_mapping.keys()}

        # send current states to the user interface if changes occurred
        for fn, subscribers in self._data_update_mapping.items():
            try:
                exec_result = fn()
            except Exception as e:
                exec_result = e

            if data_update_mem[fn] != exec_result:
                for subscriber in subscribers:

                    serialized_result = exec_result.to_json() if isinstance(exec_result, DataModelBase)\
                                        else JSONEncoder().encode(exec_result)

                    await self._sio.emit(serialized_result,
                                         to=subscriber)

    async def add_data_subscription(self, sid: str, fn: Callable[[], Any]):
        subscribers = self._data_update_mapping[fn]
        if sid not in subscribers:
            subscribers.append(sid)

    async def remove_data_subscription(self, sid: str, fn: Callable[[], Any]):
        subscribers = self._data_update_mapping[fn]
        if sid in subscribers:
            subscribers.remove(sid)

    async def stop(self):
        self._signal_stop = True
