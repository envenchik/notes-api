import sqlite3

from notes_app.db import get_db


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


def get_notes_db(
    category_filter, created_date_filter, search, sort, order, limit, offset
):
    query = "SELECT * FROM notes"
    conditions = []
    values = []

    if category_filter:
        conditions.append("category = ?")
        values.append(category_filter)

    if created_date_filter:
        conditions.append("created_at LIKE ?")
        values.append(created_date_filter + "%")

    if search:
        conditions.append("(title LIKE ? OR content LIKE ?)")
        values.append(f"%{search}%")
        values.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if sort == "id":
        query += f" ORDER BY {sort} {order.upper()}"
    else:
        query += f" ORDER BY {sort} {order.upper()}, id {order.upper()}"

    query += " LIMIT ? OFFSET ?"
    values.extend([limit, offset])

    db = get_db()

    cursor = db.execute(query, tuple(values))

    rows = cursor.fetchall()

    notes = rows_to_notes(rows)

    return notes


def get_note_by_id_db(note_id):
    db = get_db()

    cursor = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,))

    row = cursor.fetchone()

    note = row_to_note(row)

    return note


def create_note_db(title, content, category):
    db = get_db()

    try:
        cursor = db.execute(
            "INSERT INTO notes (title, content, category) VALUES (?, ?, ?)",
            (title, content, category),
        )

        new_note_id = cursor.lastrowid
        db.commit()
    except sqlite3.Error:
        db.rollback()
        raise

    new_note = get_note_by_id_db(new_note_id)

    return new_note


def update_note_db(note_id, title, content, category):
    db = get_db()

    try:
        cursor = db.execute(
            "UPDATE notes SET title = ?, content = ?, category = ? WHERE id = ?",
            (title, content, category, note_id),
        )

        if cursor.rowcount == 0:
            return None

        db.commit()
    except sqlite3.Error:
        db.rollback()
        raise

    updated_note = get_note_by_id_db(note_id)

    return updated_note


def delete_note_db(note_id):
    db = get_db()

    try:
        cursor = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))

        if cursor.rowcount == 0:
            return False

        db.commit()
    except sqlite3.Error:
        db.rollback()
        raise

    return True
