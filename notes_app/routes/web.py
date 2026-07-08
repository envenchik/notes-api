from flask import Blueprint, redirect, render_template, request, url_for

from notes_app.services.note_service import (
    get_notes_service,
    create_note_service,
    update_note_service,
    delete_note_service,
)

web_bp = Blueprint("web", __name__)


@web_bp.route("/notes-page", methods=["GET"])
def get_notes_page():
    query_params = request.args.to_dict()

    notes, error = get_notes_service(query_params)

    if error is not None:
        return render_template("notes.html", notes=[], error=error["message"]), 400

    return render_template("notes.html", notes=notes, error=None), 200


@web_bp.route("/notes-page", methods=["POST"])
def create_note_page():
    title = request.form.get("title")
    content = request.form.get("content")
    category = request.form.get("category")

    data = {"title": title, "content": content, "category": category}

    _, error = create_note_service(data)

    if error is not None:
        notes, _ = get_notes_service()
        return render_template("notes.html", notes=notes, error=error["message"]), 400

    return redirect(url_for("web.get_notes_page"))


@web_bp.route("/notes-page/update/<int:note_id>", methods=["POST"])
def update_note_page(note_id):
    title = request.form.get("title")
    content = request.form.get("content")
    category = request.form.get("category")

    data = {"title": title, "content": content, "category": category}

    _, error = update_note_service(note_id, data)

    if error is not None and error["message"] == "Note not found":
        notes, _ = get_notes_service()
        return render_template("notes.html", notes=notes, error=error["message"]), 404

    if error is not None:
        notes, _ = get_notes_service()
        return render_template("notes.html", notes=notes, error=error["message"]), 400

    return redirect(url_for("web.get_notes_page"))


@web_bp.route("/notes-page/delete/<int:note_id>", methods=["POST"])
def delete_note_page(note_id):
    _, error = delete_note_service(note_id)

    if error is not None:
        notes, _ = get_notes_service()
        return render_template("notes.html", notes=notes, error=error["message"]), 404

    return redirect(url_for("web.get_notes_page"))
