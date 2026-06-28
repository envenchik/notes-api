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
- Filtering notes by category and created date
- Basic HTML interface
- Basic request validation
- Routes, services and repositories layers

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Health check |
| GET | `/notes` | Get notes with optional filters |
| GET | `/notes/<id>` | Get note by ID |
| POST | `/notes` | Create note |
| PUT | `/notes/<id>` | Update note |
| DELETE | `/notes/<id>` | Delete note |

## Filters

Notes can be filtered by category and created date.

## Web Interface

`/notes-page` provides a basic HTML interface for viewing, creating, updating, deleting and filtering notes.

## Note Example

```json
{
  "title": "Note",
  "content": "Example",
  "category": "Learning"
}
```