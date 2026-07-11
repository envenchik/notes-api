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
- Pagination with limit and offset
- Basic HTML interface
- Basic request validation
- Routes, services and repositories layers

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/` | Health check |
| GET | `/api/notes` | Get notes with optional filtering, search and sorting |
| GET | `/api/notes/<id>` | Get note by ID |
| POST | `/api/notes` | Create note |
| PUT | `/api/notes/<id>` | Update note |
| DELETE | `/api/notes/<id>` | Delete note |

## Query Options

`GET /api/notes` supports these optional query parameters:

| Parameter | Example | Description |
| --- | --- | --- |
| `category` | `/api/notes?category=Learning` | Filter by category |
| `created_date` | `/api/notes?created_date=2000-01-01` | Filter by creation date prefix |
| `search` | `/api/notes?search=Example` | Search in title and content |
| `sort` | `/api/notes?sort=title` | Sort by `id`, `title`, or `created_at` |
| `order` | `/api/notes?order=asc` | Sort order: `asc` or `desc` |
| `limit` | `/api/notes?limit=10` | Maximum number of notes to return; default `20`, allowed range `1–100` |
| `offset` | `/api/notes?offset=20` | Number of notes to skip; default `0`, allowed range `0–1000000` |

## Errors

API errors use this format:

```json
{
  "error": {
    "code": "invalid_title",
    "message": "Title must be a non-empty string"
  }
}
```
Invalid input returns `400`. Missing resources return `404`. Unsupported methods return `405`.

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