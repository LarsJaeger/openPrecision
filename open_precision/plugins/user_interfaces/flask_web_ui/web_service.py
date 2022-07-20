from __future__ import annotations

import os
import secrets
from multiprocessing.managers import SyncManager
from typing import TYPE_CHECKING

from flask import Flask, render_template, send_from_directory
from flask_caching import Cache
from flask_socketio import SocketIO, emit

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.interfaces.user_interface import UserInterface
from open_precision.custom_sync_manager import CustomSyncManager

if TYPE_CHECKING:
    from open_precision.manager import Manager


class FlaskWebUI(UserInterface):
    def __init__(self, manager: Manager):
        self.man: Manager = manager
        # self.start()

    def start(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        template_dir = os.path.join(basedir, os.path.relpath('./templates'))
        static_dir = os.path.join(basedir, os.path.relpath('./static'))
        app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        app.config['SECRET_KEY'] = secrets.token_hex(16)
        socketio = SocketIO(app)

        @app.route('/')
        def index():
            return render_template("index.html")

        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(os.path.join(app.root_path, 'static'),
                                       'favicon.ico', mimetype='image/vnd.microsoft.icon')

        @socketio.on('connect')
        def test_connect(data):
            print('[INFO]: client connected')
            sync_manager = CustomSyncManager(("127.0.0.1", 50000), authkey=b'open_precision')
            sync_manager.connect()
            man = sync_manager.Manager
            print(f'A {man}')
            man.plugins[Navigator].course = man.plugins[CourseGenerator].generate_course()
            d = man.plugins[Navigator].course
            emit('course', {'Course': d.as_json()})

        @socketio.on('disconnect')
        def test_disconnect():
            print('[INFO]: client disconnected')

        socketio.run(app)

    def cleanup(self):
        pass

    def get_input(self, description: str, type: type) -> any:
        # TODO
        pass

    def show_message(self, message: str, message_type: str):
        # TODO
        pass
