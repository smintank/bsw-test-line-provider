from decimal import Decimal

import pytest

from models import Event
from services.event_services import EventService


@pytest.mark.asyncio
async def test_get_events(test_db, mock_event_repository) -> None:
    """Проверяет, что есть события в БД."""
    event = await EventService(event_repo=mock_event_repository).get_or_fetch_event(
        test_db, 1
    )

    assert event is not None
    assert isinstance(event, Event)
    assert event.id == 1
    assert event.coefficient == Decimal("1.5")
