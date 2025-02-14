import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from repositories.bets import BetRepository
from models.bets import Bet, EventStatus


@pytest.mark.asyncio
async def test_create_and_get_bet(db_session: AsyncSession):

    bet_data = {
        "amount": Decimal("10.0"),
        "event_id": 1,
        "coefficient": Decimal("1.5"),
        "status": EventStatus.NOT_FINISHED
    }

    bet = Bet(**bet_data)
    bet_id = await BetRepository.create_bet(db_session, bet)

    bet_from_db = await db_session.get(Bet, bet_id)

    assert bet_from_db is not None
    assert bet_from_db.amount == Decimal("10.0")
    assert bet_from_db.event_id == 1
    assert bet_from_db.coefficient == Decimal("1.5")
    assert bet_from_db.status == EventStatus.NOT_FINISHED


@pytest.mark.asyncio
async def test_get_all_bets(db_session: AsyncSession):

    bet1 = Bet(amount=Decimal("5.0"), event_id=2, coefficient=Decimal("1.2"), status=EventStatus.NOT_FINISHED)
    bet2 = Bet(amount=Decimal("15.0"), event_id=3, coefficient=Decimal("1.8"), status=EventStatus.WIN)

    db_session.add_all([bet1, bet2])
    await db_session.commit()

    bets = await BetRepository.get_all_bets(db_session)

    assert len(bets) >= 2
    assert any(bet.event_id == 2 for bet in bets)
    assert any(bet.event_id == 3 for bet in bets)