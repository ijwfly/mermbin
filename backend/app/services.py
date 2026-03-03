import secrets
import string
from datetime import datetime, timedelta, timezone

from app.config import TTL_MAP
from app.database import get_db

BASE62 = string.ascii_letters + string.digits


def generate_id(length: int = 8) -> str:
    return "".join(secrets.choice(BASE62) for _ in range(length))


def compute_expires_at(ttl: str) -> str | None:
    seconds = TTL_MAP[ttl]
    if seconds is None:
        return None
    dt = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    return dt.isoformat()


async def create_paste(
    content: str,
    content_type: str,
    language: str | None,
    ttl: str,
) -> dict:
    db = get_db()
    paste_id = generate_id()
    created_at = datetime.now(timezone.utc).isoformat()
    expires_at = compute_expires_at(ttl)

    await db.execute(
        "INSERT INTO pastes (id, content, content_type, language, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)",
        (paste_id, content, content_type, language, created_at, expires_at),
    )
    await db.commit()

    return {
        "id": paste_id,
        "url": f"/p/{paste_id}",
        "created_at": created_at,
        "expires_at": expires_at,
    }


async def get_paste(paste_id: str) -> dict | None:
    db = get_db()
    cursor = await db.execute("SELECT * FROM pastes WHERE id = ?", (paste_id,))
    row = await cursor.fetchone()
    if row is None:
        return None

    # Check expiration
    expires_at = row["expires_at"]
    if expires_at is not None:
        if datetime.fromisoformat(expires_at) < datetime.now(timezone.utc):
            return None

    return {
        "id": row["id"],
        "content": row["content"],
        "content_type": row["content_type"],
        "language": row["language"],
        "created_at": row["created_at"],
        "expires_at": row["expires_at"],
    }
