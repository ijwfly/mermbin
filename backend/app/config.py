import os
from pathlib import Path

DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", Path(__file__).parent.parent / "pastes.db"))
MAX_PASTE_SIZE = 512 * 1024  # 512 KB
CLEANUP_INTERVAL_SECONDS = 60

TTL_MAP = {
    "1h": 3600,
    "1d": 86400,
    "1w": 604800,
    "1m": 2592000,
    "never": None,
}
