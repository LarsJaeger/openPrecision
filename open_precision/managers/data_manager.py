from __future__ import annotations

import json
from typing import TYPE_CHECKING, Dict

from socketio.asyncio_redis_manager import AsyncRedisManager
from socketio.asyncio_server import AsyncServer

from open_precision.core.model import DataModelBase
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.core.plugin_base_classes.vehicle_state_builder import VehicleStateBuilder

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class DataManager:
    def __init__(self, manager: SystemHub):
        self._signal_stop = False
        self._manager = manager
        self._sio_queue = None
        self._data_update_mapping: Dict[str, Callable[[], Any]] = {
            "target_machine_state": lambda: self._manager.plugins[Navigator].target_machine_state.to_json(with_rels=[Course.CONTAINS]),
            "course": lambda: self._manager.plugins[Navigator].course.to_json(),
            "vehicle_state": lambda: self._manager.plugins[VehicleStateBuilder].vehicle_state.to_json(),
        }

    async def start_update_loop(self):
        url = 'redis://redis:6379'
        self._sio_queue = AsyncServer(client_manager=AsyncRedisManager(url),
                                      async_mode='asgi',
                                      cors_allowed_origins="*")
        while not self._signal_stop:
            await self.update()
            # await asyncio.sleep(10)

    async def update(self):
        try:
            # handle actions and deliver responses
            await self._manager.system_task_manager.handle_tasks(amount=10)

            data_update_mem = {k: None for k in self._data_update_mapping.keys()}

            # send current states to the user interface if changes occured
            for key, fn in self._data_update_mapping.items():
                exec_result = fn()
                if data_update_mem[key] != exec_result:
                    await self._sio_queue.emit(key, exec_result,
                                               room=key)
        except Exception as e:
            await self._sio_queue.emit('error', str(e),
                                       room='error')

    async def stop(self):
        self._signal_stop = True
