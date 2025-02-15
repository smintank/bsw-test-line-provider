from unittest.mock import AsyncMock

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from db.session import Base

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DB_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture(scope="function")
async def test_db():
    """Создает и удаляет тестовую БД перед и после каждого теста."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = TestingSessionLocal()
    yield session
    await session.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
