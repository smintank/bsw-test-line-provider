import os

import httpx
import pytest_asyncio
import asyncio

import respx
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from services.event_services import LineProviderService

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from main import app
from db.session import Base, get_db


test_engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)

def override_get_db():
    async def _override():
        async with TestingSessionLocal() as session:
            yield session
    return _override


app.dependency_overrides[get_db] = override_get_db()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac

@pytest_asyncio.fixture
async def mock_external_api():
    async with respx.mock:
        respx.get("http://line-provider:8000/events/1/").respond(
            json={"id": 1, "status": 1},
            status_code=200
        )
        yield

@pytest_asyncio.fixture(autouse=True)
async def mock_http_client():
    """Подменяем HTTP-клиент в тестах"""
    LineProviderService._client = httpx.AsyncClient()
    yield
    await LineProviderService.close_client()