from notes_app.repositories.note_repository import (
    get_all_notes_db,
    get_note_by_id_db,
    create_note_db,
    update_note_db,
    delete_note_db,
)


def validate_note_data(data):
    if not isinstance(data, dict):
        return None, "Invalid JSON"

    title = data.get("title")
    content = data.get("content")
    category = data.get("category")

    if not isinstance(title, str) or title.strip() == "":
        return None, "Title is required"

    if not isinstance(content, str) or content.strip() == "":
        return None, "Content is required"

    if not isinstance(category, str) or category.strip() == "":
        return None, "Category is required"

    clean_data = {
        "title": title.strip(),
        "content": content.strip(),
        "category": category.strip(),
    }

    return clean_data, None


def get_all_notes_service():
    notes = get_all_notes_db()

    return notes, None


def get_note_by_id_service(note_id):
    note = get_note_by_id_db(note_id)

    if note is None:
        return None, "Note not found"

    return note, None


def create_note_service(data):
    clean_data, error = validate_note_data(data)

    if error is not None:
        return None, error

    new_note = create_note_db(
        clean_data["title"],
        clean_data["content"],
        clean_data["category"],
    )

    return new_note, None


def update_note_service(note_id, data):
    clean_data, error = validate_note_data(data)

    if error is not None:
        return None, error

    updated_note = update_note_db(
        note_id,
        clean_data["title"],
        clean_data["content"],
        clean_data["category"],
    )

    if updated_note is None:
        return None, "Note not found"

    return updated_note, None


def delete_note_service(note_id):
    deleted = delete_note_db(note_id)

    if not deleted:
        return None, "Note not found"

    return deleted, None
