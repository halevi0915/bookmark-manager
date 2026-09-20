# Bookmark Manager

A tiny, self-hosted bookmark manager for localhost/personal use. Built with FastAPI,
a flat text file as the "database," and a minimalist dark UI.

## Features

- Add bookmarks with a URL, name, and category
- List bookmarks grouped by category
- Delete bookmarks
- Data stored in a single plain text file (easy to back up, edit by hand, or version)

## Data format

Each line in `data/bookmarks.txt` is:

```
url|name|category
```

Avoid using `|` inside a name or category — it's the field separator.

## Getting started

### Clone

```bash
git clone https://github.com/halevi0915/bookmark-manager.git
cd bookmark-manager
```

### Run locally (no Docker)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit http://localhost:8000

### Run with Docker

```bash
docker compose up --build
```

Visit http://localhost:8000

Bookmarks are saved to `./data/bookmarks.txt` on your host machine (mounted into
the container), so your data survives container rebuilds.

## Project structure

```
bookmark-manager/
├── main.py              # FastAPI app: load/save + get/add/delete endpoints
├── templates/
│   └── index.html       # UI, server-rendered
├── static/
│   └── style.css        # dark minimalist styling
├── data/
│   └── bookmarks.txt    # created at runtime, this is your "db"
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Endpoints

| Method | Path              | Description                  |
|--------|-------------------|-------------------------------|
| GET    | `/`                | HTML page, bookmarks by category |
| GET    | `/bookmarks`       | Raw JSON list of all bookmarks |
| POST   | `/bookmarks`       | Add a bookmark (form: url, name, category) |
| DELETE | `/bookmarks/{id}`  | Delete bookmark by index |
