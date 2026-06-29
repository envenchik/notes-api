from flask import Blueprint, jsonify, request

from notes_app.services.note_service import (
    get_notes_service,
    get_note_by_id_service,
    create_note_service,
    update_note_service,
    delete_note_service,
)

api_bp = Blueprint("api", __name__)


@api_bp.route("/")
def index():
    return jsonify({"message": "Notes API is running!"})


@api_bp.route("/notes", methods=["GET"])
def get_notes():
    category_filter = request.args.get("category")
    created_date_filter = request.args.get("created_date")
    search = request.args.get("search")
    sort = request.args.get("sort")
    order = request.args.get("order")

    notes, error = get_notes_service(
        category_filter=category_filter,
        created_date_filter=created_date_filter,
        search=search,
        sort=sort,
        order=order,
    )

    if error is not None:
        return jsonify({"error": error}), 400

    return jsonify(notes), 200


@api_bp.route("/notes/<int:note_id>", methods=["GET"])
def get_note_by_id(note_id):
    note, error = get_note_by_id_service(note_id)

    if error is not None:
        return jsonify({"error": error}), 404

    return jsonify(note), 200


@api_bp.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True)

    new_note, error = create_note_service(data)

    if error is not None:
        return jsonify({"error": error}), 400

    return jsonify(new_note), 201


@api_bp.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json(silent=True)

    updated_note, error = update_note_service(note_id, data)

    if error == "Note not found":
        return jsonify({"error": error}), 404

    if error is not None:
        return jsonify({"error": error}), 400

    return jsonify(updated_note), 200


@api_bp.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    _, error = delete_note_service(note_id)

    if error is not None:
        return jsonify({"error": error}), 404

    return "", 204
