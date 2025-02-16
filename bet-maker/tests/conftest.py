from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.session import Base
from models import Event
from repositories.bets import BetRepository
from repositories.evants import EventRepository

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


@pytest_asyncio.fixture
async def add_event_to_db(test_db) -> Event:
    """Добавляет событие в базу и возвращает его"""
    event = Event(
        coefficient=Decimal(1),
        deadline=datetime.now() + timedelta(minutes=1),
    )
    test_db.add(event)
    await test_db.flush()
    await test_db.commit()
    return event


@pytest_asyncio.fixture
async def mocked_event_service():
    """Мокирует весь EventService"""
    with patch("services.event_services.EventService", autospec=True) as mock_service:
        instance = mock_service.return_value
        instance.get_or_fetch_event.return_value = Event(
            id=1,
            coefficient=Decimal("1.5"),
            deadline=datetime.now() + timedelta(minutes=1),
        )
        yield instance


@pytest_asyncio.fixture
async def mock_event_repository() -> AsyncMock:
    """Мокирует весь EventRepository"""
    mock_repo = AsyncMock(spec=EventRepository)
    mock_repo.get_one.return_value = Event(
        id=1, coefficient=Decimal("1.5"), deadline=datetime.now() + timedelta(minutes=1)
    )
    return mock_repo


@pytest_asyncio.fixture
async def bet_repo() -> BetRepository:
    return BetRepository()
