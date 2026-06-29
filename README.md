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
- Searching notes by title and content
- Sorting notes by ID, title and creation date
- Basic HTML interface
- Basic request validation
- Routes, services and repositories layers

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Health check |
| GET | `/notes` | Get notes with optional filtering, search and sorting |
| GET | `/notes/<id>` | Get note by ID |
| POST | `/notes` | Create note |
| PUT | `/notes/<id>` | Update note |
| DELETE | `/notes/<id>` | Delete note |

## Query Options

Notes can be filtered by category and created date.

Notes can be searched by title and content.

Notes can be sorted by ID, title and creation date.

## Web Interface

`/notes-page` provides a basic HTML interface for viewing, creating, updating, deleting, filtering, searching and sorting notes.

## Note Example

```json
{
  "title": "Note",
  "content": "Example",
  "category": "Learning"
}
```