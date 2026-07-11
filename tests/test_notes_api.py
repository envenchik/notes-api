from notes_app.db import get_db


def insert_note(
    app, title="Test title", content="Test content", category="Test category"
):
    with app.app_context():
        connection = get_db()
        cursor = connection.execute(
            "INSERT INTO notes (title, content, category) VALUES (?, ?, ?)",
            (title, content, category),
        )
        connection.commit()
        return cursor.lastrowid


def test_init_db_command(runner):
    result = runner.invoke(args=["init-db"])

    assert result.exit_code == 0
    assert "Initialized the database." in result.output


def test_invalid_url(client):
    response = client.get("/api/unknown")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "not_found"


def test_invalid_method(client):
    response = client.patch("/api/notes")

    assert response.status_code == 405
    assert response.get_json()["error"]["code"] == "method_not_allowed"


def test_get_notes_empty(client):
    response = client.get("/api/notes")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_notes_returns_all(app, client):
    for _ in range(10):
        insert_note(app)

    response = client.get("/api/notes")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 10


def test_get_note_by_id(app, client):
    note_id = insert_note(app)

    response = client.get(f"/api/notes/{note_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == note_id


def test_get_note_by_id_not_found(client):
    response = client.get("/api/notes/1")

    assert response.status_code == 404


def test_create_note(client):
    response = client.post(
        "/api/notes",
        json={
            "title": "Test title",
            "content": "Test content",
            "category": "Test category",
        },
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["title"] == "Test title"
    assert data["content"] == "Test content"
    assert data["category"] == "Test category"
    assert "id" in data
    assert "created_at" in data

    note_id = data["id"]
    response = client.get(f"/api/notes/{note_id}")

    assert response.status_code == 200


def test_create_note_with_empty_title_returns_400(client):
    response = client.post(
        "/api/notes",
        json={
            "title": "",
            "content": "Test content",
            "category": "Test category",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_title"


def test_create_note_with_missing_field_returns_400(client):
    response = client.post(
        "/api/notes",
        json={
            "content": "Test content",
            "category": "Test category",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_body"


def test_create_note_with_invalid_field_type_returns_400(client):
    response = client.post(
        "/api/notes",
        json={
            "title": 1,
            "content": "Test content",
            "category": "Test category",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_title"


def test_create_note_without_json_returns_400(client):
    response = client.post("/api/notes")

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_json"


def test_create_note_with_json_array_body_returns_400(client):
    response = client.post("/api/notes", json=[1, 2, 3])

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_body"


def test_create_note_with_extra_field_returns_400(client):
    response = client.post(
        "/api/notes",
        json={
            "title": "Test title",
            "content": "Test content",
            "category": "Test category",
            "created_at": "2000-01-01",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_body"


def test_update_note(app, client):
    note_id = insert_note(app)

    response = client.put(
        f"/api/notes/{note_id}",
        json={
            "title": "Updated",
            "content": "Updated",
            "category": "Updated",
        },
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["title"] == "Updated"
    assert data["content"] == "Updated"
    assert data["category"] == "Updated"

    response = client.get(f"/api/notes/{note_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["title"] == "Updated"
    assert data["content"] == "Updated"
    assert data["category"] == "Updated"


def test_update_note_not_found(client):
    response = client.put(
        "/api/notes/1",
        json={
            "title": "Updated",
            "content": "Updated",
            "category": "Updated",
        },
    )

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "note_not_found"


def test_update_note_with_invalid_data_returns_400(client, app):
    note_id = insert_note(app)

    response = client.put(
        f"/api/notes/{note_id}",
        json={
            "title": "",
            "content": "Updated",
            "category": "Updated",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_title"


def test_delete_note(app, client):
    note_id = insert_note(app)

    response = client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 204

    response = client.get(f"/api/notes/{note_id}")
    assert response.status_code == 404


def test_delete_note_not_found(client):
    response = client.delete("/api/notes/1")
    assert response.status_code == 404


def test_get_notes_with_extra_query_param_returns_400(client):
    response = client.get("/api/notes", query_string={"unknown": ""})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "unknown_query_parameter"


def test_get_notes_filters_by_category(client, app):
    for _ in range(5):
        insert_note(app)

    insert_note(app, category="target")

    response = client.get("/api/notes", query_string={"category": "target"})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["category"] == "target"


def test_get_notes_filters_with_empty_category_returns_400(client):
    response = client.get("/api/notes", query_string={"category": ""})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_category_filter"


def test_get_notes_filters_by_created_date(client):
    response = client.get("/api/notes", query_string={"created_date": "2000-01-01"})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0


def test_get_notes_filters_with_empty_created_date_returns_400(client):
    response = client.get("/api/notes", query_string={"created_date": ""})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_created_date_filter"


def test_get_notes_filters_with_invalid_created_date_returns_400(client):
    response = client.get("/api/notes", query_string={"created_date": "2000-01-01x"})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_created_date_filter"


def test_get_notes_searches_by_text(client, app):
    for _ in range(5):
        insert_note(app)

    insert_note(app, title="target")
    insert_note(app, content="target")

    response = client.get("/api/notes", query_string={"search": "target"})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2

    for note in data:
        assert "target" in note["title"] or "target" in note["content"]


def test_get_notes_with_empty_search_returns_400(client):
    response = client.get("/api/notes", query_string={"search": ""})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_search"


def test_get_notes_sorts_by_title_asc(client, app):
    for _ in range(5):
        insert_note(app)

    insert_note(app, title="A")

    response = client.get("/api/notes", query_string={"sort": "title", "order": "asc"})

    assert response.status_code == 200
    assert response.get_json()[0]["title"] == "A"


def test_get_notes_with_empty_sort_returns_400(client):
    response = client.get("/api/notes", query_string={"sort": ""})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_sort"


def test_get_notes_with_invalid_sort_returns_400(client):
    response = client.get("/api/notes", query_string={"sort": "error"})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_sort"


def test_get_notes_with_empty_order_returns_400(client):
    response = client.get("/api/notes", query_string={"order": ""})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_order"


def test_get_notes_with_invalid_order_returns_400(client):
    response = client.get("/api/notes", query_string={"order": "error"})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "invalid_order"


def test_get_notes_limit(app, client):
    for _ in range(10):
        insert_note(app)

    response = client.get("/api/notes", query_string={"limit": "5"})

    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_notes_default_limit(app, client):
    for _ in range(21):
        insert_note(app)

    response = client.get("/api/notes")

    assert response.status_code == 200
    assert len(response.get_json()) == 20


def test_get_notes_limit_out_of_range(client):
    response = client.get("/api/notes", query_string={"limit": "101"})

    assert response.get_json()["error"]["code"] == "invalid_limit"
    assert response.status_code == 400


def test_get_notes_with_empty_limit(client):
    response = client.get("/api/notes", query_string={"limit": ""})

    assert response.get_json()["error"]["code"] == "invalid_limit"
    assert response.status_code == 400


def test_get_notes_offset(app, client):
    for _ in range(2):
        insert_note(app)

    response = client.get("/api/notes", query_string={"offset": "1"})

    assert response.status_code == 200
    assert response.get_json()[0]["id"] == 1


def test_get_notes_offset_out_of_range(client):
    response = client.get("/api/notes", query_string={"offset": "10000001"})

    assert response.get_json()["error"]["code"] == "invalid_offset"
    assert response.status_code == 400


def test_get_notes_with_empty_offset(client):
    response = client.get("/api/notes", query_string={"offset": ""})

    assert response.get_json()["error"]["code"] == "invalid_offset"
    assert response.status_code == 400


def test_get_notes_pagination(app, client):
    for _ in range(6):
        insert_note(app)

    first_page = client.get(
        "/api/notes",
        query_string={"limit": "2", "offset": "0"},
    )
    second_page = client.get(
        "/api/notes",
        query_string={"limit": "2", "offset": "2"},
    )

    assert [note["id"] for note in first_page.get_json()] == [6, 5]
    assert [note["id"] for note in second_page.get_json()] == [4, 3]
