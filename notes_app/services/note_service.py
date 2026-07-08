import re

from notes_app.repositories.note_repository import (
    get_notes_db,
    get_note_by_id_db,
    create_note_db,
    update_note_db,
    delete_note_db,
)

ALLOWED_DATA_FIELDS = {"title", "content", "category"}
ALLOWED_QUERY_PARAMS = {"category", "created_date", "search", "sort", "order"}
ALLOWED_SORT_FIELDS = {"id", "title", "created_at"}
ALLOWED_ORDERS = {"asc", "desc"}

CREATED_DATE_PATTERN = r"\d{4}-\d{2}-\d{2}"

DEFAULT_SORT = "created_at"
DEFAULT_ORDER = "desc"


def error_response(code, message):
    return {"code": code, "message": message}


def validate_note_data(data):
    if data is None:
        return None, error_response("invalid_json", "Request body must be valid JSON")

    if not isinstance(data, dict):
        return None, error_response(
            "invalid_body",
            "Request body must be a JSON object with title, content and category",
        )

    title = data.get("title")
    content = data.get("content")
    category = data.get("category")

    if set(data.keys()) != ALLOWED_DATA_FIELDS:
        return None, error_response(
            "invalid_body",
            "Request body must be a JSON object with title, content and category",
        )

    if not isinstance(title, str) or title.strip() == "":
        return None, error_response("invalid_title", "Title must be a non-empty string")

    if not isinstance(content, str) or content.strip() == "":
        return None, error_response(
            "invalid_content", "Content must be a non-empty string"
        )

    if not isinstance(category, str) or category.strip() == "":
        return None, error_response(
            "invalid_category", "Category must be a non-empty string"
        )

    clean_data = {
        "title": title.strip(),
        "content": content.strip(),
        "category": category.strip(),
    }

    return clean_data, None


def validate_query_params(query_params):
    category_filter = query_params.get("category")
    created_date_filter = query_params.get("created_date")
    search = query_params.get("search")
    sort = query_params.get("sort")
    order = query_params.get("order")

    for query_param in query_params.keys():
        if query_param not in ALLOWED_QUERY_PARAMS:
            return None, error_response(
                "unknown_query_parameter",
                "Unknown query parameter",
            )

    if category_filter is None:
        category_filter = None
    elif category_filter.strip() == "":
        return None, error_response(
            "invalid_category_filter", "Category filter must be a non-empty string"
        )
    else:
        category_filter = category_filter.strip()

    if created_date_filter is None:
        created_date_filter = None
    elif created_date_filter.strip() == "" or not re.fullmatch(
        CREATED_DATE_PATTERN, created_date_filter.strip()
    ):
        return None, error_response(
            "invalid_created_date_filter",
            "Created date filter must match the pattern: YYYY-MM-DD",
        )
    else:
        created_date_filter = created_date_filter.strip()

    if search is None:
        search = None
    elif search.strip() == "":
        return None, error_response(
            "invalid_search", "Search must be a non-empty string"
        )
    else:
        search = search.strip()

    if sort is None:
        sort = DEFAULT_SORT
    elif sort.strip().lower() not in ALLOWED_SORT_FIELDS:
        return None, error_response(
            "invalid_sort", "Sort must be one of: id, title, created_at"
        )
    else:
        sort = sort.strip().lower()

    if order is None:
        order = DEFAULT_ORDER
    elif order.strip().lower() not in ALLOWED_ORDERS:
        return None, error_response("invalid_order", "Order must be one of: asc, desc")
    else:
        order = order.strip().lower()

    clean_query_params = {
        "category_filter": category_filter,
        "created_date_filter": created_date_filter,
        "search": search,
        "sort": sort,
        "order": order,
    }

    return clean_query_params, None


def get_notes_service(query_params=None):
    if query_params is None:
        query_params = {}

    clean_query_params, error = validate_query_params(query_params)

    if error is not None:
        return None, error

    notes = get_notes_db(
        category_filter=clean_query_params["category_filter"],
        created_date_filter=clean_query_params["created_date_filter"],
        search=clean_query_params["search"],
        sort=clean_query_params["sort"],
        order=clean_query_params["order"],
    )

    return notes, None


def get_note_by_id_service(note_id):
    note = get_note_by_id_db(note_id)

    if note is None:
        return None, error_response("note_not_found", "Note not found")

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
        return None, error_response("note_not_found", "Note not found")

    return updated_note, None


def delete_note_service(note_id):
    deleted = delete_note_db(note_id)

    if not deleted:
        return None, error_response("note_not_found", "Note not found")

    return deleted, None
