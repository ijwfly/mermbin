import asyncio
from datetime import datetime, timezone

from app.config import CLEANUP_INTERVAL_SECONDS
from app.database import get_db


async def cleanup_loop() -> None:
    while True:
        try:
            db = get_db()
            now = datetime.now(timezone.utc).isoformat()
            await db.execute(
                "DELETE FROM pastes WHERE expires_at IS NOT NULL AND expires_at < ?",
                (now,),
            )
            await db.commit()
        except Exception:
            pass
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)
