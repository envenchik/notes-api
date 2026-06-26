import sqlite3

from pathlib import Path
from config import DATABASE_NAME

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


def init_db() -> None:
    database_path = Path(DATABASE_NAME)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    sql_script = SCHEMA_PATH.read_text(encoding="utf-8")

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.executescript(sql_script)

    connection.commit()
    connection.close()

    print("Database initialized.")


if __name__ == "__main__":
    init_db()
