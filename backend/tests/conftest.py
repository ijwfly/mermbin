import httpx
import pytest
from httpx import ASGITransport

import app.database as database
from app.database import init_db, close_db
from app.main import app


@pytest.fixture()
async def test_db(tmp_path):
    db_path = tmp_path / "test.db"
    database.DATABASE_PATH = db_path
    await init_db()
    yield
    await close_db()


@pytest.fixture()
async def client(test_db):
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
