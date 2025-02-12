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
    async with AsyncClient() as client:
        response = await client.get(settings.line_provider_url.format(settings.bet_maker_host))
        if response.status_code != 200:
            raise ValueError(f"Ошибка запроса: {response.status_code}, ответ: {response.text}")
        if "application/json" not in response.headers.get("Content-Type", ""):
            raise ValueError(f"Ответ не является JSON: {response.text}")
        return response.json()
