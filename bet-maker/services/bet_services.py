from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.bets import Bet
from repositories.bets import BetRepository
from schemas.bet_schemas import CreateBetSchema
from services.event_services import EventService


class BetService:
    @staticmethod
    async def create_new_bet(db: AsyncSession, bet_data: CreateBetSchema) -> Bet:
        """Создает новую ставку"""
        event = await EventService.get_or_create_event(db, bet_data.event_id)
        if not event:
            raise HTTPException(
                status_code=404,
                detail={"message": 'Нельзя сделать ставку на это событие'})

        new_bet = Bet(
            amount=bet_data.amount,
            coefficient=Decimal(event.coefficient),
            event=event,
        )
        return await BetRepository.create_bet(db, new_bet)
