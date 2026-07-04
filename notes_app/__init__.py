from pathlib import Path
from flask import Flask
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

    return app
