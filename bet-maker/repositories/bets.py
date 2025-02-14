from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.bets import Bet
from schemas.bet_schemas import GetBetsSchema
from schemas.event_schemas import EventSchema


class BetRepository:

    @staticmethod
    async def create_bet(db: AsyncSession, bet: Bet) -> Bet:
        """Создает ставку в базе данных."""
        db.add(bet)
        await db.commit()
        await db.refresh(bet)
        return bet

    @staticmethod
    async def get_all_bets(db: AsyncSession) -> list[GetBetsSchema]:
        result = await db.execute(
            select(Bet).options(joinedload(Bet.event))
        )
        bets = result.scalars().all()

        return [
            GetBetsSchema(
                id=bet.id,
                amount=bet.amount,
                event=EventSchema(
                    event_id=bet.event.id,
                    coefficient=bet.event.coefficient,
                    deadline=bet.event.deadline,
                    status=bet.event.status
                )
            )
            for bet in bets
        ]
