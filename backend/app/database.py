import aiosqlite

from app.config import DATABASE_PATH

_db: aiosqlite.Connection | None = None


async def init_db() -> None:
    global _db
    _db = await aiosqlite.connect(DATABASE_PATH)
    _db.row_factory = aiosqlite.Row
    await _db.execute("""
        CREATE TABLE IF NOT EXISTS pastes (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            content_type TEXT NOT NULL,
            language TEXT,
            created_at TEXT NOT NULL,
            expires_at TEXT
        )
    """)
    await _db.execute("""
        CREATE INDEX IF NOT EXISTS idx_pastes_expires_at ON pastes (expires_at)
    """)
    await _db.commit()


def get_db() -> aiosqlite.Connection:
    assert _db is not None, "Database not initialized"
    return _db


async def close_db() -> None:
    global _db
    if _db is not None:
        await _db.close()
        _db = None
