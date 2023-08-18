from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Callable, Awaitable, Any

import uvicorn

import open_precision.api.dependencies as dependencies  # this must be imported before other api modules
from open_precision.api import server as main_server
from open_precision.api.server import app

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class API:
    """
    responsible for initializing and starting the (not really REST-ful) API
    """

    def __init__(self, queue_task: Callable[[Callable[[SystemHub], Any]], Awaitable[Any]]):
        self._thread: None | threading.Thread = None
        self.queue_task = queue_task
        self.app = main_server.app
        self._server: uvicorn.Server | None = None

        # inject queue_task into dependencies
        dependencies._global_queue_task_func = queue_task

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._server is not None:
            self._server.should_exit = True
            self._thread.join()

    def __enter__(self):
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _run(self):
        main_server.queue_task = self.queue_task
        config = uvicorn.Config(app, host="0.0.0.0",
                                log_level="info")  # , ssl_keyfile="key.pem", ssl_certfile="cert.pem")
        self._server = uvicorn.Server(config=config)
        self._server.run()
