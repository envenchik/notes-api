import sqlite3

from config import DATABASE_NAME


def get_db_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    return connection


def row_to_note(row):
    if row is None:
        return None

    note = {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "category": row["category"],
        "created_at": row["created_at"],
    }

    return note


def rows_to_notes(rows):
    notes = [row_to_note(row) for row in rows]

    return notes


def get_all_notes_db():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes ORDER BY id")

    rows = cursor.fetchall()

    connection.close()

    notes = rows_to_notes(rows)

    return notes


def get_note_by_id_db(note_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))

    row = cursor.fetchone()

    connection.close()

    note = row_to_note(row)

    return note


def create_note_db(title, content, category):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO notes (title, content, category) VALUES (?, ?, ?)",
        (title, content, category),
    )

    new_note_id = cursor.lastrowid

    connection.commit()
    connection.close()

    new_note = get_note_by_id_db(new_note_id)

    return new_note


def update_note_db(note_id, title, content, category):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE notes SET title = ?, content = ?, category = ? WHERE id = ?",
        (title, content, category, note_id),
    )

    if cursor.rowcount == 0:
        connection.close()
        return None

    connection.commit()
    connection.close()

    updated_note = get_note_by_id_db(note_id)

    return updated_note


def delete_note_db(note_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    if cursor.rowcount == 0:
        connection.close()
        return False

    connection.commit()
    connection.close()

    return True
