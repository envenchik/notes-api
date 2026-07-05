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
    assert response.get_json()["error"] == "Invalid title"


def test_create_note_with_missing_field_returns_400(client):
    response = client.post(
        "/api/notes",
        json={
            "content": "Test content",
            "category": "Test category",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid title"


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
    assert response.get_json()["error"] == "Invalid title"


def test_create_note_without_json_returns_400(client):
    response = client.post("/api/notes")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid JSON"


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
    assert response.get_json()["error"] == "Note not found"


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
    assert response.get_json()["error"] == "Invalid title"


def test_delete_note(app, client):
    note_id = insert_note(app)

    response = client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 204

    response = client.get(f"/api/notes/{note_id}")
    assert response.status_code == 404


def test_delete_note_not_found(client):
    response = client.delete("/api/notes/1")
    assert response.status_code == 404


def test_get_notes_filters_by_category(client, app):
    for _ in range(5):
        insert_note(app)

    insert_note(app, category="target")

    response = client.get("/api/notes", query_string={"category": "target"})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["category"] == "target"


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


def test_get_notes_sorts_by_title_asc(client, app):
    for _ in range(5):
        insert_note(app)

    insert_note(app, title="A")

    response = client.get("/api/notes", query_string={"sort": "title", "order": "asc"})

    assert response.status_code == 200
    assert response.get_json()[0]["title"] == "A"
