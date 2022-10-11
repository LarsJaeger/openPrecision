from __future__ import annotations
from typing import TYPE_CHECKING

import socketio

from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.manager import Manager


class ActionManager:
    def __init__(self, manager: Manager):
        self._manager: Manager = manager

        url = 'redis://redis:6379'
        self._sio_queue: socketio.AsyncServer = socketio.AsyncServer(
            client_manager=socketio.AsyncRedisManager(url), async_handlers=False)

        @self._sio_queue.on("action")
        async def on_action(data):
            print("alalalalaction")
            match data:
                case "gen_course":
                    self._manager.plugins[Navigator].course = self._manager.plugins[CourseGenerator].generate_course()
