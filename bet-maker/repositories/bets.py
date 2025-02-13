from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.bets import Bet


class BetRepository:

    @staticmethod
    async def create_bet(db: AsyncSession, bet: Bet) -> int:
        db.add(bet)
        await db.commit()
        await db.refresh(bet)
        return bet.id

    @staticmethod
    async def get_all_bets(db: AsyncSession) -> list[Bet]:
        result = await db.execute(select(Bet))
        return list(result.scalars().all())
