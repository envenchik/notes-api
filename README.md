# Notes API

Notes API is a learning project for practicing backend development with Python and Flask.

The goal of this project is to build a small backend application step by step and gradually improve it while learning new backend concepts.

## Stack

- Python
- Flask
- SQLite
- Raw SQL

## Features

- JSON API
- CRUD operations for notes
- Basic HTML interface
- Basic request validation
- Routes, services and repositories layers

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Health check |
| GET | `/notes` | Get all notes |
| GET | `/notes/<id>` | Get note by ID |
| POST | `/notes` | Create note |
| PUT | `/notes/<id>` | Update note |
| DELETE | `/notes/<id>` | Delete note |

## Web Interface

`/notes-page` provides a basic HTML interface for viewing, creating, updating and deleting notes.

## Note Example

```json
{
  "title": "Note",
  "content": "Example",
  "category": "Learning"
}
```