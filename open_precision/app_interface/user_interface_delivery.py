from __future__ import annotations

import os.path
from enum import Enum
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from open_precision.utils import async_partial

if TYPE_CHECKING:
    from open_precision.manager import Manager


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


# quasi class methods

async def websocket_endpoint(self: UserInterfaceDelivery, websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


async def get_index(self: UserInterfaceDelivery):
    return self._templates.TemplateResponse("item.html", {"request": request, "id": id})


class UserInterfaceDelivery:
    def __init__(self, manager: Manager):
        self._manager = manager

        self._base_dir = os.path.dirname(__file__)
        self._templates = Jinja2Templates(directory=os.path.join(self._base_dir, os.path.relpath("./templates")))
        self._app = FastAPI()
        # socket_manager = SocketManager(app=self._app)

        self._app.get("/", include_in_schema=False, response_class=HTMLResponse)(async_partial(get_index, self))
        # self._app.mount("/", StaticFiles(directory=os.path.join(self._base_dir, os.path.relpath("./static")), html=True), name="static")

        self._app.websocket("/websocket_endpoint", name='websocket_endpoint')(
            async_partial(websocket_endpoint, self))

    def show_message(self, message: str, message_type: MessageType):
        pass

    def get_input(self, description: str, input_data_type: type) -> any:
        pass
