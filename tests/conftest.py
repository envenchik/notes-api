import pytest

from notes_app import create_app
from notes_app.db import init_db


@pytest.fixture()
def app(tmp_path):
    app = create_app(
        test_config={
            "TESTING": True,
            "DATABASE": str(tmp_path / "test_notes.db"),
        }
    )

    with app.app_context():
        init_db()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
