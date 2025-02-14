from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from repositories.bets import BetRepository
from schemas.bet_schemas import CreateBetSchema, GetBetsSchema, CreatedBetResponseSchema
from services.bet_services import BetService

router = APIRouter()


@router.post("/bet/", response_model=CreatedBetResponseSchema)
async def make_bet(bet: CreateBetSchema, db: AsyncSession = Depends(get_db)):
    bet = await BetService.create_new_bet(db, bet)
    return CreatedBetResponseSchema.model_validate({"bet_id": bet.id})


@router.get("/bets/", response_model=list[GetBetsSchema])
async def get_bets(db: AsyncSession = Depends(get_db)):
    bets = await BetRepository.get_all_bets(db)
    return [GetBetsSchema.model_validate(bet) for bet in bets]
