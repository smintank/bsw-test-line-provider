from datetime import datetime, timedelta
from decimal import Decimal

import pytest
import pytest_asyncio
from sqlalchemy import select

from models import Bet
from models.events import Event, EventStatus
from routes.events import get_available_events


def test_bet_status_enum():

    assert EventStatus.NOT_FINISHED.value == "not_finished"
    assert EventStatus.WIN.value == "win"
    assert EventStatus.LOSE.value == "lose"


@pytest.fixture
def valid_event_data():
    return {
        "id": 1,
        "coefficient": Decimal("2.5"),
        "deadline": datetime.now() + timedelta(days=1),
        "status": EventStatus.NOT_FINISHED,
    }


@pytest.fixture
def invalid_event_data():
    pass


@pytest.fixture
def valid_bet_data(add_event_to_db):
    return {
        "amount": Decimal("50.0"),
        "coefficient": Decimal("3.0"),
        "event": add_event_to_db,
    }


@pytest.fixture
def invalid_bet_data():
    pass


@pytest.mark.asyncio
async def test_create_event(test_db, valid_event_data):
    """Тест создания события"""
    event = Event(**valid_event_data)

    test_db.add(event)
    await test_db.flush()
    await test_db.commit()

    assert event.id == valid_event_data["id"]
    assert event.coefficient == valid_event_data["coefficient"]
    assert event.deadline == valid_event_data["deadline"]
    assert event.status == valid_event_data["status"]


@pytest.mark.asyncio
async def test_create_bet(test_db, valid_bet_data):
    """Тест создания ставки и связи с событием"""
    bet = Bet(**valid_bet_data)

    test_db.add(bet)
    await test_db.flush()
    await test_db.commit()

    assert bet.id is not None
    assert bet.id == 1
    assert bet.event_id == valid_bet_data.get("event").id
    assert bet.event.status == valid_bet_data.get("event").status
    assert bet.event.deadline == valid_bet_data.get("event").deadline
    assert bet.amount == valid_bet_data.get("amount")
    assert bet.coefficient == valid_bet_data.get("coefficient")
    assert isinstance(bet.timestamp, datetime)


@pytest.mark.asyncio
async def test_cascade_delete_event(test_db):
    """Тест каскадного удаления - при удалении Event, удаляются все связанные Bet"""
    event = Event(
        coefficient=Decimal("1.8"),
        deadline=datetime.now() + timedelta(days=1),
    )

    test_db.add(event)
    await test_db.flush()

    bet = Bet(amount=Decimal("100.0"), coefficient=Decimal("1.8"), event=event)
    test_db.add(bet)
    await test_db.flush()
    await test_db.commit()

    event_id = event.id

    await test_db.delete(event)
    await test_db.commit()

    event_check = await test_db.get(Event, event_id)
    assert event_check is None

    bet_check = await test_db.execute(select(Bet).filter(Bet.event_id == event_id))
    assert bet_check.scalars().first() is None
