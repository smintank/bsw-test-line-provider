from decimal import Decimal

import pytest
import pytest_asyncio
from fastapi import HTTPException
from pydantic_core import ValidationError

import messages
from repositories.evants import EventRepository
from schemas.bet_schemas import CreateBetSchema
from services.bet_services import BetService
from services.event_services import EventService
from services.line_provider_api_service import LineProviderAPIService


@pytest_asyncio.fixture
async def event_service() -> EventService:
    return EventService(
        event_repo=EventRepository(), api_service=LineProviderAPIService()
    )


@pytest_asyncio.fixture
async def get_create_bet_schema(test_db) -> CreateBetSchema:
    return CreateBetSchema(event_id=1, amount=Decimal("10.0"))


@pytest_asyncio.fixture
async def get_bet_service_event_mocked(
    test_db, bet_repo, mocked_event_service, get_create_bet_schema
) -> BetService:
    bet_service = BetService(bet_repo=bet_repo, event_service=mocked_event_service)
    await bet_service.create_new_bet(test_db, get_create_bet_schema)
    return bet_service


@pytest.mark.asyncio
async def test_get_all_bets_empty(test_db, bet_repo) -> None:
    """Проверяет, что без ставок список пуст."""
    bet_service = BetService(bet_repo=bet_repo)
    bets = await bet_service.get_all_available_bets(test_db)
    assert bets == []


@pytest.mark.asyncio
async def test_create_bet(
    test_db, mocked_event_service, get_create_bet_schema, bet_repo
) -> None:
    """Проверяет создание ставки с валидным event_id"""
    bet_service = BetService(bet_repo=bet_repo, event_service=mocked_event_service)
    bet = await bet_service.create_new_bet(test_db, get_create_bet_schema)

    assert bet.bet_id == 1


@pytest.mark.parametrize("event_id", ["1", 2, 10])
@pytest.mark.asyncio
async def test_create_bet_with_not_existed_event(
    test_db, event_id, bet_repo, event_service
) -> None:
    """Проверяет создание ставки с валидным event_id"""
    bet_data = CreateBetSchema(event_id=event_id, amount=Decimal("10.0"))
    with pytest.raises(HTTPException) as exc_info:
        bet_service = BetService(bet_repo=bet_repo, event_service=event_service)
        await bet_service.create_new_bet(test_db, bet_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {"message": messages.EVENT_NOT_EXISTS}


@pytest.mark.parametrize("event_id", ["test", -1, 0])
@pytest.mark.asyncio
async def test_create_bet_with_wrong_event(
    test_db, event_id, bet_repo, mocked_event_service
) -> None:
    """Проверяет создание ставки с невалидными event_id"""
    with pytest.raises(ValidationError) as exc_info:
        bet_data = CreateBetSchema(event_id=event_id, amount=Decimal("10.0"))
        bet_service = BetService(bet_repo=bet_repo, event_service=mocked_event_service)
        await bet_service.create_new_bet(test_db, bet_data)

    assert exc_info.type == ValidationError


@pytest.mark.asyncio
async def test_create_bet_and_get_all_bets(
    test_db, get_create_bet_schema, mocked_event_service, bet_repo
) -> None:
    """Добавляет ставку и проверяет, что она в списке."""
    bet_service = BetService(bet_repo=bet_repo, event_service=mocked_event_service)
    await bet_service.create_new_bet(test_db, get_create_bet_schema)

    bets = await bet_service.get_all_available_bets(test_db)
    assert len(bets) == 1
    assert bets[0].id == get_create_bet_schema.event_id
    assert bets[0].amount == get_create_bet_schema.amount
