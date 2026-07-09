import sqlite3

from pathlib import Path
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from . import db
from notes_app.routes.api import api_bp
from notes_app.routes.web import web_bp


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=str(Path(app.instance_path) / "notes.db"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_http_exception(http_error):
        if request.path.startswith("/api/"):
            response = {
                "error": {
                    "code": http_error.name.lower().replace(" ", "_"),
                    "message": http_error.description,
                }
            }

            return jsonify(response), http_error.code

        return http_error

    @app.errorhandler(sqlite3.Error)
    def handle_db_exception(db_error):
        if request.path.startswith("/api/"):
            response = {
                "error": {
                    "code": "database_error",
                    "message": "Database error",
                }
            }

            return jsonify(response), 500

        return "Internal Server Error", 500
