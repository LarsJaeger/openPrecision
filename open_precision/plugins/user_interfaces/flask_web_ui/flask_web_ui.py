from __future__ import annotations

import os
from typing import TYPE_CHECKING
from flask import Flask, render_template

from open_precision.core.interfaces.user_interface import UserInterface

if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class FlaskWebUI(UserInterface):
    def __init__(self, manager: Manager):
        template_dir = os.path.abspath('../open_precision/plugins/user_interfaces/flask_web_ui/templates')
        app = Flask(__name__, template_folder=template_dir)

        @app.route('/')
        def index():
            return render_template("app.html")

        app.run()

    def cleanup(self):
        pass
