from datetime import datetime, timedelta, timezone

import pytest

from app.database import get_db


class TestPostPaste:
    async def test_create_text(self, client):
        resp = await client.post("/api/pastes", json={
            "content": "hello world",
            "content_type": "text",
        })
        assert resp.status_code == 201
        body = resp.json()
        assert "id" in body
        assert "url" in body
        assert body["url"] == f"/p/{body['id']}"

    async def test_create_code(self, client):
        resp = await client.post("/api/pastes", json={
            "content": "print(1)",
            "content_type": "code",
            "language": "python",
        })
        assert resp.status_code == 201

    async def test_create_mermaid(self, client):
        resp = await client.post("/api/pastes", json={
            "content": "graph TD; A-->B;",
            "content_type": "mermaid",
        })
        assert resp.status_code == 201

    async def test_empty_content_422(self, client):
        resp = await client.post("/api/pastes", json={
            "content": "",
            "content_type": "text",
        })
        assert resp.status_code == 422

    async def test_missing_language_422(self, client):
        resp = await client.post("/api/pastes", json={
            "content": "x = 1",
            "content_type": "code",
            "language": None,
        })
        assert resp.status_code == 422

    async def test_invalid_type_422(self, client):
        resp = await client.post("/api/pastes", json={
            "content": "hello",
            "content_type": "html",
        })
        assert resp.status_code == 422


class TestGetPaste:
    async def test_get_existing(self, client):
        create = await client.post("/api/pastes", json={
            "content": "test content",
            "content_type": "text",
        })
        paste_id = create.json()["id"]

        resp = await client.get(f"/api/pastes/{paste_id}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["content"] == "test content"
        assert body["content_type"] == "text"

    async def test_get_nonexistent_404(self, client):
        resp = await client.get("/api/pastes/nonexistent")
        assert resp.status_code == 404

    async def test_get_expired_404(self, client):
        db = get_db()
        expired_at = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        await db.execute(
            "INSERT INTO pastes (id, content, content_type, language, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("expired99", "old", "text", None, datetime.now(timezone.utc).isoformat(), expired_at),
        )
        await db.commit()

        resp = await client.get("/api/pastes/expired99")
        assert resp.status_code == 404

    async def test_roundtrip(self, client):
        cases = [
            {"content": "plain text", "content_type": "text"},
            {"content": "print('hi')", "content_type": "code", "language": "python"},
            {"content": "graph LR; A-->B;", "content_type": "mermaid"},
        ]
        for payload in cases:
            create = await client.post("/api/pastes", json=payload)
            assert create.status_code == 201
            paste_id = create.json()["id"]

            get = await client.get(f"/api/pastes/{paste_id}")
            assert get.status_code == 200
            assert get.json()["content"] == payload["content"]
            assert get.json()["content_type"] == payload["content_type"]
