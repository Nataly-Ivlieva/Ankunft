import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.base import Base
from app.db.session import get_session


DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
async def admin_token(client):
    # signup admin
    resp = await client.post(
        "/auth/signup",
        json={
            "email": "admin@test.de",
            "password": "admin123",
            "role": "admin",
        },
    )
    assert resp.status_code == 200
    return resp.json()["token"]


@pytest.fixture
async def user_token(client):
    # signup normal user
    resp = await client.post(
        "/auth/signup",
        json={
            "email": "user@test.de",
            "password": "user123",
            "role": "user",
        },
    )
    assert resp.status_code == 200
    return resp.json()["token"]

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac
