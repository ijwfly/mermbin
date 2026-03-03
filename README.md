# Mermbin

Pastebin with Mermaid diagram rendering, code syntax highlighting, and pan/zoom support.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Vue](https://img.shields.io/badge/Vue-3-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Features

- **Mermaid diagrams** — live preview while editing, pan & zoom on view
- **Code** — syntax highlighting via highlight.js (190+ languages)
- **Plain text** — simple paste sharing
- **Auto-expiry** — TTL options: 1 hour, 1 day, 1 week, 1 month, or never
- **No auth required** — anonymous paste creation
- **One-command deploy** — single Docker container, SQLite storage

## Quick Start

```bash
docker-compose up -d
```

Open http://localhost:8000

## Tech Stack

- **Backend:** FastAPI + SQLite (aiosqlite)
- **Frontend:** Vue 3, Mermaid.js, highlight.js, panzoom
- **Deploy:** Multi-stage Docker build (Node 22 + Python 3.12)

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/pastes` | Create a paste |
| `GET` | `/api/pastes/{id}` | Get a paste |

### Create paste

```bash
curl -X POST http://localhost:8000/api/pastes \
  -H "Content-Type: application/json" \
  -d '{"content": "graph TD\n  A-->B", "content_type": "mermaid", "ttl": "1d"}'
```

`content_type`: `mermaid`, `code`, `text`
`ttl`: `1h`, `1d`, `1w`, `1m`, `never`

## Local Development

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app, static file serving
│   │   ├── routes.py       # API endpoints
│   │   ├── services.py     # Business logic
│   │   ├── database.py     # SQLite via aiosqlite
│   │   ├── models.py       # Pydantic schemas
│   │   ├── config.py       # Settings (DB path, TTL, limits)
│   │   └── cleanup.py      # Background task for expired pastes
│   └── tests/
├── frontend/
│   └── src/
│       ├── views/          # CreateView, PasteView
│       └── components/     # MermaidPreview, CodeHighlight, PanZoom
├── Dockerfile              # Multi-stage build
└── docker-compose.yml      # One-command deploy
```
