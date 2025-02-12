from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models import Bet
from schemas import SCreateBet, SEvent, EventState


async def create_bet(db: AsyncSession, bet: SCreateBet) -> int:
    new_bet = Bet(amount=bet.amount, event_id=bet.event_id)
    db.add(new_bet)
    await db.commit()
    await db.refresh(new_bet)
    return new_bet.id


async def get_all_bets(db: AsyncSession) -> list[Bet]:
    result = await db.execute(select(Bet))
    return list(result.scalars().all())


async def fetch_all_events() -> list[SEvent]:
    if settings.is_single:
        return [SEvent(event_id=1, status=EventState.FINISHED_WIN, coefficient=1.43, deadline=234234234234),
                SEvent(event_id=1, status=EventState.FINISHED_LOSE, coefficient=1.43, deadline=234234234234)]
    url = settings.events_url
    async with AsyncClient() as client:
        response = await client.get(url)
        events = await response.json()
        return events
