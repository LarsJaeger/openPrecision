from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from open_precision.api.config import config_router

if TYPE_CHECKING:
    pass


class MessageType(Enum):
    """
    Enum for the different message types.
    """
    INFO = 0
    DEBUG = 1
    WARNING = 2
    SUCCESS = 3
    CRITICAL = 4
    ERROR = 5


class API:
    def __init__(self, task_queue):
        url = 'redis://redis:6379'

        self.app = FastAPI()

        # serve the static frontend
        self.app.mount("", StaticFiles(directory="/app/open_precision_frontend"), name="static")
        self.app.mount("/", StaticFiles(directory="/app/open_precision_frontend/index.html"), name="static")

        # include the api routes
        routers = []
        self.app.include_router(config_router)

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", log_level="info")  # , ssl_keyfile="key.pem", ssl_certfile="cert.pem")

    def show_message(self, message: str, message_type: MessageType):
        pass

    def get_input(self, description: str, input_data_type: type) -> any:
        pass
