from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.bets import Bet
from models.events import Event
from repositories.bets import BetRepository


@pytest.mark.asyncio
async def test_create_bet(test_db: AsyncSession, add_event_to_db: Event) -> None:

    bet_data = {
        "amount": Decimal("10.0"),
        "event": add_event_to_db,
        "coefficient": Decimal("1.5"),
    }

    bet = Bet(**bet_data)
    bet_from_db = await BetRepository.create(test_db, bet)

    assert bet_from_db is not None
    assert bet_from_db.amount == Decimal("10.0")
    assert bet_from_db.event_id == 1
    assert bet_from_db.coefficient == Decimal("1.5")


@pytest.mark.asyncio
async def test_get_all_bets(test_db: AsyncSession):
    bet1 = Bet(amount=Decimal("5.0"), event_id=2, coefficient=Decimal("1.2"))
    bet2 = Bet(amount=Decimal("15.0"), event_id=3, coefficient=Decimal("1.8"))

    test_db.add_all([bet1, bet2])
    await test_db.commit()

    bets = await BetRepository.get_all(test_db)
    assert len(bets) == 2

    bet1, bet2 = bets
    assert bet1.id == 1
    assert bet2.id == 2
