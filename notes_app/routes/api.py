from flask import Blueprint, jsonify, request

from notes_app.services.note_service import (
    get_notes_service,
    get_note_by_id_service,
    create_note_service,
    update_note_service,
    delete_note_service,
)


def error_json(error, status_code):
    return jsonify({"error": error}), status_code


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/")
def index():
    return jsonify({"message": "Notes API is running!"})


@api_bp.route("/notes", methods=["GET"])
def get_notes():
    query_params = request.args.to_dict()

    notes, error = get_notes_service(query_params)

    if error is not None:
        return error_json(error, 400)

    return jsonify(notes), 200


@api_bp.route("/notes/<int:note_id>", methods=["GET"])
def get_note_by_id(note_id):
    note, error = get_note_by_id_service(note_id)

    if error is not None:
        return error_json(error, 404)

    return jsonify(note), 200


@api_bp.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True)

    new_note, error = create_note_service(data)

    if error is not None:
        return error_json(error, 400)

    return jsonify(new_note), 201


@api_bp.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json(silent=True)

    updated_note, error = update_note_service(note_id, data)

    if error is not None and error["code"] == "note_not_found":
        return error_json(error, 404)

    if error is not None:
        return error_json(error, 400)

    return jsonify(updated_note), 200


@api_bp.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    _, error = delete_note_service(note_id)

    if error is not None:
        return error_json(error, 404)

    return "", 204
