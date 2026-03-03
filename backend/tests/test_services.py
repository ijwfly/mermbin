import string
from datetime import datetime, timedelta, timezone

import pytest

from app.services import generate_id, compute_expires_at, create_paste, get_paste
from app.database import get_db

BASE62 = set(string.ascii_letters + string.digits)


class TestGenerateId:
    def test_default_length(self):
        assert len(generate_id()) == 8

    def test_charset(self):
        id_ = generate_id()
        assert all(c in BASE62 for c in id_)

    def test_uniqueness(self):
        ids = {generate_id() for _ in range(100)}
        assert len(ids) == 100

    def test_custom_length(self):
        assert len(generate_id(length=12)) == 12


class TestComputeExpiresAt:
    def test_never(self):
        assert compute_expires_at("never") is None

    def test_1h(self):
        before = datetime.now(timezone.utc)
        result = compute_expires_at("1h")
        after = datetime.now(timezone.utc)

        dt = datetime.fromisoformat(result)
        assert before + timedelta(seconds=3600) <= dt <= after + timedelta(seconds=3600)


class TestCreatePaste:
    @pytest.mark.usefixtures("test_db")
    async def test_returns_dict(self):
        result = await create_paste("hello", "text", None, "1d")
        assert set(result.keys()) == {"id", "url", "created_at", "expires_at"}

    @pytest.mark.usefixtures("test_db")
    async def test_url_format(self):
        result = await create_paste("hello", "text", None, "1d")
        assert result["url"] == f"/p/{result['id']}"

    @pytest.mark.usefixtures("test_db")
    async def test_never_ttl(self):
        result = await create_paste("hello", "text", None, "never")
        assert result["expires_at"] is None


class TestGetPaste:
    @pytest.mark.usefixtures("test_db")
    async def test_existing(self):
        created = await create_paste("hello", "text", None, "1d")
        paste = await get_paste(created["id"])
        assert paste is not None
        assert paste["content"] == "hello"
        assert paste["content_type"] == "text"

    @pytest.mark.usefixtures("test_db")
    async def test_nonexistent(self):
        assert await get_paste("nonexistent") is None

    @pytest.mark.usefixtures("test_db")
    async def test_expired(self):
        # Insert a paste with an already-expired timestamp
        db = get_db()
        expired_at = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        await db.execute(
            "INSERT INTO pastes (id, content, content_type, language, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("expired1", "old", "text", None, datetime.now(timezone.utc).isoformat(), expired_at),
        )
        await db.commit()

        assert await get_paste("expired1") is None
