from __future__ import annotations

import json
import multiprocessing
import os
import threading
from typing import TYPE_CHECKING

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.interfaces.user_interface import UserInterface

if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class FlaskWebUI(UserInterface):
    def __init__(self, manager: Manager):
        self.man: Manager = manager
        self.start()

    def start(self):
        template_dir = os.path.abspath('../open_precision/plugins/user_interfaces/flask_web_ui/templates')
        static_dir = os.path.abspath('../open_precision/plugins/user_interfaces/flask_web_ui/static')
        app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        socketio = SocketIO(app)

        @app.route('/')
        def index():
            return render_template("index.html")

        @socketio.on('connect')
        def test_connect(auth):
            print('[INFO]: client connected')
            self.man.plugins[Navigator].course = self.man.plugins[CourseGenerator].generate_course()
            d = self.man.plugins[Navigator].course
            data = d.asdict()
            print(f"data: {data}, bla: {str(d)}")
            emit('course', {'Course': data})

        @socketio.on('disconnect')
        def test_disconnect():
            print('[INFO]: client disconnected')

        socketio.run(app)

    def cleanup(self):
        pass
