from datetime import datetime, timedelta, timezone

import pytest

from app.database import get_db


async def insert_paste(id_, expires_at):
    db = get_db()
    await db.execute(
        "INSERT INTO pastes (id, content, content_type, language, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)",
        (id_, "content", "text", None, datetime.now(timezone.utc).isoformat(), expires_at),
    )
    await db.commit()


async def paste_exists(id_) -> bool:
    db = get_db()
    cursor = await db.execute("SELECT 1 FROM pastes WHERE id = ?", (id_,))
    return await cursor.fetchone() is not None


async def run_cleanup_once():
    """Execute one cleanup iteration without the infinite loop."""
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "DELETE FROM pastes WHERE expires_at IS NOT NULL AND expires_at < ?",
        (now,),
    )
    await db.commit()


@pytest.mark.usefixtures("test_db")
class TestCleanup:
    async def test_deletes_expired(self):
        expired = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        await insert_paste("exp1", expired)

        await run_cleanup_once()
        assert not await paste_exists("exp1")

    async def test_keeps_valid(self):
        future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        await insert_paste("valid1", future)

        await run_cleanup_once()
        assert await paste_exists("valid1")

    async def test_keeps_never_expire(self):
        await insert_paste("never1", None)

        await run_cleanup_once()
        assert await paste_exists("never1")

    async def test_mixed(self):
        expired = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

        await insert_paste("mix_exp", expired)
        await insert_paste("mix_valid", future)
        await insert_paste("mix_never", None)

        await run_cleanup_once()
        assert not await paste_exists("mix_exp")
        assert await paste_exists("mix_valid")
        assert await paste_exists("mix_never")
