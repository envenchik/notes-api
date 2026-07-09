import sqlite3
import pytest

from notes_app.db import get_db


def test_db_rejects_empty_title(app):
    with app.app_context():
        db = get_db()

        with pytest.raises(sqlite3.IntegrityError):
            db.execute(
                "INSERT INTO notes (title, content, category) VALUES (?, ?, ?)",
                ("", "Test content", "Test category"),
            )

        db.rollback()


def test_db_rejects_null_title(app):
    with app.app_context():
        db = get_db()

        with pytest.raises(sqlite3.IntegrityError):
            db.execute(
                "INSERT INTO notes (content, category) VALUES (?, ?)",
                ("Test content", "Test category"),
            )

        db.rollback()
