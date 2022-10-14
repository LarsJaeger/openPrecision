from __future__ import annotations
from typing import TYPE_CHECKING

from socketio.asyncio_redis_manager import AsyncRedisManager
from socketio.asyncio_server import AsyncServer

from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.manager import Manager


class ActionManager:
    def __init__(self, manager: Manager):
        self._manager: Manager = manager

        url = 'redis://redis:6379'
        self._sio_queue: AsyncServer = AsyncServer(client_manager=AsyncRedisManager(url),
                                                   async_mode='asgi',
                                                   cors_allowed_origins="*")
        @self._sio_queue.on("action")
        async def on_action(data):
            print("alalalalaction")
            match data:
                case "gen_course":
                    self._manager.plugins[Navigator].course = self._manager.plugins[CourseGenerator].generate_course()

    def handle_actions(self):
