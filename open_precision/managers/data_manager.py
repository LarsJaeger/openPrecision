from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

import socketio

from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.manager import Manager


class DataManager:
    def __init__(self, manager: Manager):
        self._manager = manager

        url = 'redis://'
        self._sio_queue = socketio.AsyncServer(
            client_manager=socketio.AsyncRedisManager(url))

    async def update_loop(self):
        # while True:
        await asyncio.gather(self.update(), asyncio.sleep(10))

    async def update(self):
        current_target_machine_state = self._manager.plugins[Navigator].target_machine_state
        await self._sio_queue.emit('data', data=current_target_machine_state.as_json(),
                                   room='target_current_machine_state')
