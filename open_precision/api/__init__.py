from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Awaitable, Any

import uvicorn

import open_precision.api.dependencies as dependencies  # this must be imported before other api modules
from open_precision.api import server
from open_precision.api.server import app

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class API:
    def __init__(self, queue_task: Callable[[Callable[[SystemHub], Any]], Awaitable[Any]]):
        self.queue_task = queue_task
        self.app = server.app

        # inject queue_task into dependencies
        dependencies._global_queue_task_func = queue_task

    def run(self):
        server.queue_task = self.queue_task
        uvicorn.run(app, host="0.0.0.0", log_level="info")  # , ssl_keyfile="key.pem", ssl_certfile="cert.pem")
