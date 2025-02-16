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


#
# @pytest.mark.parametrize("seconds", (-1, 0, 1, -10, 10))
# @pytest_asyncio.fixture
# async def test_wrong_deadline(test_db, add_event_to_db, mocked_repository, seconds) -> None:
#     deadline = add_event_to_db.deadline
#     deadline = datetime.now() - timedelta(seconds=seconds)
#
#     event = await EventService.get_or_fetch_event(test_db, add_event_to_db.id, mocked_repository)
#
#     assert event == []
