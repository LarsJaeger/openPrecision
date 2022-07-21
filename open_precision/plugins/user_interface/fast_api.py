from abc import ABC
from functools import partial

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import TYPE_CHECKING

from open_precision.core.interfaces.user_interface_base import UserInterface, MessageType

if TYPE_CHECKING:
    from open_precision.manager import Manager


async def websocket_endpoint(manager: Manager, websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


class FastAPIUserInterface(UserInterface):

    def __init__(self, manager: Manager):
        self._manager = manager
        self._app = FastAPI()
        self._app.mount("/", StaticFiles(directory="static", html=True), name="static")
        self._app.websocket("/websocket_endpoint")(partial(websocket_endpoint, self._manager))

    def show_message(self, message: str, message_type: MessageType):
        pass

    def get_input(self, description: str, type: type) -> any:
        pass
