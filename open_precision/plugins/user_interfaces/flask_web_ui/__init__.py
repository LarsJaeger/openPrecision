from __future__ import annotations

from typing import TYPE_CHECKING
from flask import Flask, render_template

from open_precision.core.interfaces.user_interface import UserInterface

if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager

class FlaskWebUI(UserInterface):
    def __init__(self, manager: Manager):
        app = Flask(__name__)
        app.run()

        @app.route('/')
        def index(self):
            return render_template(app.html)

    def _cleanup(self):
        pass