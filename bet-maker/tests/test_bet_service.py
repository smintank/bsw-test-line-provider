from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from fastapi import HTTPException
from pydantic_core import ValidationError

import messages
from models import Event
from schemas.bet_schemas import CreateBetSchema
from services.bet_services import BetService
from services.event_services import EventService


@pytest_asyncio.fixture
async def mock_event_service():
    """Мокирует EventService.get_or_fetch_event"""
    with patch.object(EventService, "get_or_fetch_event", new_callable=AsyncMock) as mock_get_event:
        mock_get_event.return_value = Event(id=1, coefficient=Decimal("1.5"), deadline=datetime.now())
        yield mock_get_event


@pytest_asyncio.fixture
async def get_create_bet_schema(test_db) -> CreateBetSchema:
    return CreateBetSchema(event_id=1, amount=Decimal("10.0"))


@pytest.mark.asyncio
async def test_get_all_bets_empty(test_db) -> None:
    """Проверяет, что без ставок список пуст."""
    bets = await BetService.get_all_bets(test_db)
    assert bets == []

@pytest.mark.asyncio
async def test_create_bet(test_db, mock_event_service, get_create_bet_schema) -> None:
    """Проверяет создание ставки с валидным event_id"""
    bet = await BetService.create_new_bet(test_db, get_create_bet_schema)

    assert bet.id == 1
    assert bet.amount == get_create_bet_schema.amount
    assert bet.event_id == get_create_bet_schema.event_id


@pytest.mark.parametrize("event_id", [2, 10])
@pytest.mark.asyncio
async def test_create_bet_with_not_existed_event(test_db, event_id) -> None:
    """Проверяет создание ставки с валидным event_id"""
    bet_data = CreateBetSchema(event_id=event_id, amount=Decimal("10.0"))
    with pytest.raises(HTTPException) as exc_info:
        await BetService.create_new_bet(test_db, bet_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {"message": messages.EVENT_UNAVAILABLE}


@pytest.mark.parametrize("event_id", [-10, -1, 0])
@pytest.mark.asyncio
async def test_create_bet_with_wrong_event(test_db, event_id) -> None:
    """Проверяет создание ставки с валидным event_id"""
    with pytest.raises(ValidationError) as exc_info:
        bet_data = CreateBetSchema(event_id=event_id, amount=Decimal("10.0"))
        await BetService.create_new_bet(test_db, bet_data)

    assert exc_info.type == ValidationError



@pytest.mark.asyncio
async def test_create_bet_and_get_all_bets(test_db, get_create_bet_schema, mock_event_service) -> None:
    """Добавляет ставку и проверяет, что она в списке."""
    await BetService.create_new_bet(test_db, get_create_bet_schema)

    bets = await BetService.get_all_bets(test_db)
    assert len(bets) == 1
    assert bets[0].id == get_create_bet_schema.event_id
    assert bets[0].amount == get_create_bet_schema.amount
