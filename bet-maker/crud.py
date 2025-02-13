import logging

from typing import Sequence
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models import Bet
from schemas import EventSchema

logger = logging.getLogger(__name__)


async def create_bet(db: AsyncSession, bet: Bet) -> int:
    db.add(bet)
    await db.commit()
    await db.refresh(bet)
    return bet.id


async def get_all_bets(db: AsyncSession) -> Sequence[Bet]:
    result = await db.execute(select(Bet))
    return result.scalars().all()


async def get_url_data(url: str) -> dict:
    async with AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            logger.error("Ошибка запроса: %d, ответ: %d", response.status_code, response.text)
            return {}
        if "application/json" not in response.headers.get("Content-Type", ""):
            logger.error("Ответ не является JSON: %d", response.text)
            return {}
        return response.json()


async def fetch_event(event_id: int) -> EventSchema | None:
    url = f'http://line-provider:{settings.line_provider_port}/events/{str(event_id)}/'
    data = await get_url_data(url)
    return EventSchema(**data) if data else None


async def fetch_available_events() -> list[EventSchema]:
    url = f'http://line-provider:{settings.line_provider_port}/events/'
    return list(await get_url_data(url))
