from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from crud import get_all_bets, create_bet, fetch_event
from models import Bet
from schemas import CreateBetSchema, GetBetsSchema, CreatedBetResponseSchema

router = APIRouter()


@router.post("/bet/", response_model=CreatedBetResponseSchema)
async def make_bet(bet: CreateBetSchema, db: AsyncSession = Depends(get_db)):
    if event_data := await fetch_event(bet.event_id):
        new_bet = Bet(amount=bet.amount,
                      event_id=event_data.event_id,
                      status=event_data.status,
                      coefficient=event_data.coefficient)
        bet_id = await create_bet(db, new_bet)
        return CreatedBetResponseSchema(bet_id=bet_id)
    raise HTTPException(status_code=404, detail={"message": "Событие не найдено"})


@router.get("/bets/", response_model=list[GetBetsSchema])
async def get_bets(db: AsyncSession = Depends(get_db)):
    bets = await get_all_bets(db)
    return [GetBetsSchema.model_validate(bet) for bet in bets]
