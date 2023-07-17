from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Callable, Any, List

from socketio.asyncio_server import AsyncServer

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class DataManager:
    def __init__(self, manager: SystemHub):
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

        while not self._signal_stop:
            await self.update()
            # await asyncio.sleep(10)

    async def update(self):
        try:
            # handle actions and deliver responses
            await self._manager.system_task_manager.handle_tasks(amount=10)

            data_update_mem = {k: None for k in self._data_update_mapping.keys()}

            # send current states to the user interface if changes occured
            for fn, subscribers in self._data_update_mapping.items():
                exec_result = fn()
                if data_update_mem[fn] != exec_result:
                    for subscriber in subscribers:
                        await self._sio.emit(exec_result, to=subscriber)
        except Exception as e:
            await self._sio.emit('error', str(e),
                                 room='error')

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
