from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from messages import EVENT_UNAVAILABLE
from models.bets import Bet
from repositories.bets import BetRepository
from schemas.bet_schemas import CreateBetSchema, GetBetsSchema
from schemas.event_schemas import EventSchema
from services.event_services import EventService


class BetService:
    @staticmethod
    async def create_new_bet(db: AsyncSession, bet_data: CreateBetSchema) -> Bet:
        """Создает новую ставку"""
        event = await EventService.get_or_fetch_event(db, bet_data.event_id)
        if not event:
            raise HTTPException(status_code=404, detail={"message": EVENT_UNAVAILABLE})

        new_bet = Bet(
            amount=bet_data.amount,
            coefficient=Decimal(event.coefficient),
            event=event,
        )
        return await BetRepository.create_bet(db, new_bet)

    @staticmethod
    async def get_all_bets(db: AsyncSession) -> list[GetBetsSchema]:
        bets = await BetRepository.get_all_bets(db)
        return [
            GetBetsSchema(
                id=bet.id,
                amount=bet.amount,
                event=EventSchema(
                    event_id=bet.event.id,
                    coefficient=bet.event.coefficient,
                    deadline=bet.event.deadline,
                    status=bet.event.status.value
                )
            )
            for bet in bets
        ]
