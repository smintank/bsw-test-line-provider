from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.bets import Bet
from repositories.base import ItemRepositoryAbstract


class BetRepository(ItemRepositoryAbstract[Bet]):
    model = Bet

    @classmethod
    async def get_one(cls, db: AsyncSession, item_id: int) -> Bet | None:
        """Дополнительно загружает связанные события"""
        result = await db.execute(
            select(cls.model)
            .filter(Bet.id == item_id)
            .options(joinedload(cls.model.event))
        )
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list[Bet]:
        """Дополнительно загружает связанные события"""
        result = await db.execute(
            select(cls.model).options(joinedload(cls.model.event))
        )
        return list(result.scalars().all())
