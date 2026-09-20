import os
from pathlib import Path

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI(title="Bookmark Manager")

DATA_FILE = Path(os.environ.get("DATA_FILE", "data/bookmarks.txt"))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def load_bookmarks() -> list[dict]:
    """Read the flat-file db. Each line: url|name|category"""
    if not DATA_FILE.exists():
        return []
    bookmarks = []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 3:
                continue
            url, name, category = parts
            bookmarks.append({"url": url, "name": name, "category": category})
    return bookmarks


def save_bookmarks(bookmarks: list[dict]) -> None:
    """Overwrite the flat-file db with the given list."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        for b in bookmarks:
            f.write(f"{b['url']}|{b['name']}|{b['category']}\n")


@app.get("/")
def home(request: Request):
    bookmarks = load_bookmarks()
    categories: dict[str, list[dict]] = {}
    for i, b in enumerate(bookmarks):
        categories.setdefault(b["category"], []).append({**b, "id": i})
    return templates.TemplateResponse(
        request, "index.html", {"categories": categories}
    )


@app.get("/bookmarks")
def get_bookmarks():
    return load_bookmarks()


@app.post("/bookmarks")
def add_bookmark(
    url: str = Form(...),
    name: str = Form(...),
    category: str = Form(...),
):
    bookmarks = load_bookmarks()
    bookmarks.append(
        {
            "url": url.strip(),
            "name": name.strip(),
            "category": category.strip() or "uncategorized",
        }
    )
    save_bookmarks(bookmarks)
    return RedirectResponse("/", status_code=303)


@app.delete("/bookmarks/{index}")
def delete_bookmark(index: int):
    bookmarks = load_bookmarks()
    if index < 0 or index >= len(bookmarks):
        raise HTTPException(status_code=404, detail="Bookmark not found")
    bookmarks.pop(index)
    save_bookmarks(bookmarks)
    return {"status": "deleted"}
