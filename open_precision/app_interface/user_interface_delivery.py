from __future__ import annotations

import os.path
from enum import Enum
from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.websockets import WebSocketDisconnect

from open_precision.app_interface.helper import ConnectionManager
from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.core.plugin_base_classes.position_builder import PositionBuilder

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


class UserInterfaceDelivery:
    def __init__(self, manager: Manager):
        self._manager = manager

        # TODO: remove
        self._manager.plugins[Navigator].course = self._manager.plugins[CourseGenerator].generate_course()

        self._base_dir = os.path.dirname(__file__)
        self._templates = Jinja2Templates(directory=os.path.join(self._base_dir, os.path.relpath("./templates")))
        self._app = FastAPI()

        async def get_index(request: Request):
            return self._templates.TemplateResponse("index.html", {'request': request})

        self._app.get("/", include_in_schema=False, response_class=HTMLResponse)(get_index)

        async def get_favicon():
            return FileResponse(os.path.join(self._base_dir, os.path.relpath("./static/favicon.ico")))

        self._app.get("/favicon.ico", include_in_schema=False, response_class=FileResponse)(get_favicon)

        self._app.mount("/static/",
                        StaticFiles(directory=os.path.join(self._base_dir, os.path.relpath("./static")), html=True),
                        name="static")

        self._connection_manager_target_machine_state = ConnectionManager()

        # target_machine_state websocket
        async def target_machine_state_websocket(websocket: WebSocket):
            print("[INFO]: target_machine_state websocket is starting...")
            await self._connection_manager_target_machine_state.connect(websocket)
            print("[INFO]: target_machine_state websocket has started...")
            last_target_machine_state = None
            try:
                while True:
                    current_target_machine_state = self._manager.plugins[Navigator].target_machine_state
                    if current_target_machine_state != last_target_machine_state or last_target_machine_state is None:
                        last_target_machine_state = current_target_machine_state
                        await self._connection_manager_target_machine_state.unicast(
                            current_target_machine_state.as_json(), websocket)
            except WebSocketDisconnect:
                self._connection_manager_target_machine_state.disconnect(websocket)

        self._app.websocket("/ws/target_machine_state", name='target_machine_state')(target_machine_state_websocket)

        self._connection_manager_position = ConnectionManager()

        # position websocket
        async def position_websocket(websocket: WebSocket):
            print("[INFO]: Position websocket is starting...")
            await self._connection_manager_position.connect(websocket)
            print("[INFO]: Position websocket has started...")
            last_position = None
            try:
                while True:
                    current_position = self._manager.plugins[PositionBuilder].current_position
                    if current_position != last_position or last_position is None:
                        last_position = current_position
                        await self._connection_manager_position.unicast(current_position.as_json(), websocket)
            except WebSocketDisconnect:
                self._connection_manager_position.disconnect(websocket)

        self._app.websocket("/ws/position", name='position')(position_websocket)

    def run(self):
        uvicorn.run(self._app, log_level="info") #, ssl_keyfile="key.pem", ssl_certfile="cert.pem")

    def show_message(self, message: str, message_type: MessageType):
        pass

    def get_input(self, description: str, input_data_type: type) -> any:
        pass
