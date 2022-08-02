from __future__ import annotations

import os.path
import json
from enum import Enum
from functools import partial
from typing import TYPE_CHECKING, Optional

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.params import Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.websockets import WebSocketDisconnect
from pyquaternion import Quaternion

from open_precision.app_interface.helper import ConnectionManager
from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.core.plugin_base_classes.position_builder import PositionBuilder
from open_precision.utils import async_partial

if TYPE_CHECKING:
    from open_precision.manager import Manager
    from open_precision.core.model.data.data_model_base import DataModelBase


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
        self._connection_manager = ConnectionManager()

        async def get_index(request: Request):
            return self._templates.TemplateResponse("index.html", {'request': request})

        self._app.get("/", include_in_schema=False, response_class=HTMLResponse)(get_index)

        async def get_favicon():
            return FileResponse(os.path.join(self._base_dir, os.path.relpath("./static/favicon.ico")))

        self._app.get("/favicon.ico", include_in_schema=False, response_class=FileResponse)(get_favicon)

        self._app.mount("/static/",
                        StaticFiles(directory=os.path.join(self._base_dir, os.path.relpath("./static")), html=True),
                        name="static")

        # steering angle websocket
        async def steering_angle_websocket(websocket: WebSocket):
            await self._connection_manager.connect(websocket)
            print("[INFO]: Steering angle websocket has started...")
            last_steering_angle = None
            try:
                while True:
                    current_steering_angle = self._manager.plugins[Navigator].steering_angle
                    if current_steering_angle != last_steering_angle or last_steering_angle is None:
                        last_steering_angle = current_steering_angle
                        await self._connection_manager.unicast(current_steering_angle.as_json(), websocket)
            except WebSocketDisconnect:
                self._connection_manager.disconnect(websocket)

        self._app.websocket("/ws/steering_angle", name='steering_angle')(steering_angle_websocket)

        # position websocket
        async def position_websocket(websocket: WebSocket):
            await self._connection_manager.connect(websocket)
            print("[INFO]: Position websocket has started...")
            last_position = None
            try:
                while True:
                    current_position = self._manager.plugins[PositionBuilder].current_position
                    if current_position != last_position or last_position is None:
                        last_position = current_position
                        await self._connection_manager.unicast(current_position.as_json(), websocket)
            except WebSocketDisconnect:
                self._connection_manager.disconnect(websocket)

        self._app.websocket("/ws/position", name='position')(position_websocket)

    def show_message(self, message: str, message_type: MessageType):
        pass

    def get_input(self, description: str, input_data_type: type) -> any:
        pass
