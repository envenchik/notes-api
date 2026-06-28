from notes_app.repositories.note_repository import (
    get_notes_db,
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

    if title is None or not isinstance(title, str) or title.strip() == "":
        return None, "Invalid title"

    if content is None or not isinstance(content, str) or content.strip() == "":
        return None, "Invalid content"

    if category is None or not isinstance(category, str) or category.strip() == "":
        return None, "Invalid category"

    clean_data = {
        "title": title.strip(),
        "content": content.strip(),
        "category": category.strip(),
    }

    return clean_data, None


def clean_note_filters(category_filter, created_date_filter):
    if category_filter is None or category_filter.strip() == "":
        category_filter = None
    else:
        category_filter = category_filter.strip()

    if created_date_filter is None or created_date_filter.strip() == "":
        created_date_filter = None
    else:
        created_date_filter = created_date_filter.strip()

    return category_filter, created_date_filter


def get_notes_service(category_filter=None, created_date_filter=None):
    category_filter, created_date_filter = clean_note_filters(
        category_filter, created_date_filter
    )

    notes = get_notes_db(
        category_filter=category_filter, created_date_filter=created_date_filter
    )

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
