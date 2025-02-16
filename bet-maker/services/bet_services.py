from decimal import Decimal

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from messages import EVENT_UNAVAILABLE
from models.bets import Bet
from repositories.bets import BetRepository
from schemas.bet_schemas import CreateBetSchema, CreatedBetResponseSchema, GetBetsSchema
from schemas.event_schemas import EventSchema
from services.event_services import EventService


class BetService:
    def __init__(
        self,
        event_service: EventService = Depends(),
        bet_repo: BetRepository = Depends(),
    ):
        self.event_service = event_service
        self.bet_repo = bet_repo

    async def create_new_bet(
        self, db: AsyncSession, bet_data: CreateBetSchema
    ) -> CreatedBetResponseSchema:
        event = await self.event_service.get_or_fetch_event(db, bet_data.event_id)
        if not event:
            raise HTTPException(status_code=404, detail={"message": EVENT_UNAVAILABLE})

        new_bet = Bet(
            amount=bet_data.amount,
            coefficient=Decimal(event.coefficient),
            event=event,
        )
        new_bet = await self.bet_repo.create(db, new_bet)
        return CreatedBetResponseSchema.model_validate({"bet_id": new_bet.id})

    async def get_all_available_bets(self, db: AsyncSession) -> list[GetBetsSchema]:
        bets = await self.bet_repo.get_all(db)
        return [
            GetBetsSchema(
                id=bet.id,
                amount=bet.amount,
                event=EventSchema(
                    event_id=bet.event.id,
                    coefficient=bet.event.coefficient,
                    deadline=bet.event.deadline,
                    status=bet.event.status.value,
                ),
            )
            for bet in bets
        ]
