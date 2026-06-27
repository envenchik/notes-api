from flask import Flask

from notes_app.routes.api import api_bp
from notes_app.routes.web import web_bp


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    return app
