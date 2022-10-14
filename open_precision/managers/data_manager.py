from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

import socketio
from socketio.asyncio_redis_manager import AsyncRedisManager
from socketio.asyncio_server import AsyncServer
from socketio.redis_manager import RedisManager

from open_precision.core.exceptions import CourseNotSetException
from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.manager import Manager


class DataManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        self._sio_queue = None

    async def start_update_loop(self):
        url = 'redis://redis:6379'
        self._sio_queue = AsyncServer(client_manager=AsyncRedisManager(url),
                                      async_mode='asgi',
                                      cors_allowed_origins="*")
        while True:
            await self.update()
            await asyncio.sleep(10)

    async def update(self):
        try:
            target_machine_state = self._manager.plugins[Navigator].target_machine_state
            await self._sio_queue.emit('target_machine_state', target_machine_state.as_json(),
                                       room='target_machine_state')
        except CourseNotSetException:
            # TODO think about way to send errors to frontend
            print("[ERROR]: CourseNotSetException")
