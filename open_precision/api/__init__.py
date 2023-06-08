from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Awaitable, Any

import open_precision.api.dependencies as dependencies  # this must be imported before other api modules
from open_precision.api import server

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class API:
    def __init__(self, queue_task: Callable[[Callable[[SystemHub], Any]], Awaitable[Any]]):
        server.queue_task = queue_task

        # inject queue_task into dependencies
        dependencies._global_queue_task_func = queue_task

    def run(self):
        server.run()
