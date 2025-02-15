from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.bets import Bet


class BetRepository:

    @staticmethod
    async def create_bet(db: AsyncSession, bet: Bet) -> Bet:
        """Создает ставку в базе данных."""
        db.add(bet)
        await db.commit()
        await db.refresh(bet)
        return bet

    @staticmethod
    async def get_all_bets(db: AsyncSession) -> list[Bet]:
        """Возвращает все ставки из базы данных"""
        result = await db.execute(select(Bet).options(joinedload(Bet.event)))
        bets = result.scalars().all()
        return list(bets)
