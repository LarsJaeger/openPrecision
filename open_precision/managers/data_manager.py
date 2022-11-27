from __future__ import annotations
import asyncio
import traceback
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
        self._signal_stop = False
        self._manager = manager
        self._sio_queue = None

    async def start_update_loop(self):
        url = 'redis://redis:6379'
        self._sio_queue = AsyncServer(client_manager=AsyncRedisManager(url),
                                      async_mode='asgi',
                                      cors_allowed_origins="*")
        while not self._signal_stop:
            await self.update()
            await asyncio.sleep(10)

    async def update(self):
        try:
            # handle actions and deliver responses
            action_responses: list = self._manager.action.handle_actions(amount=10)
            # send all the responses to the user interface
            print("action responses: " + str(action_responses))

            for action_response in action_responses:
                pass
                await self._sio_queue.emit('action_response', action_response.to_json(),
                                            room=action_response.action.initiator)

            target_machine_state = self._manager.plugins[Navigator].target_machine_state
            await self._sio_queue.emit('target_machine_state', target_machine_state.to_json(),
                                        room='target_machine_state')

        except Exception as e:
            # TODO think about way to send errors to frontend -> error class and broadcast room
            print("[ERROR] Error during update:" + ''.join(
                traceback.format_exception(e, value=e, tb=e.__traceback__)))

    async def stop(self):
        self._signal_stop = True
