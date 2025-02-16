from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from schemas.bet_schemas import CreateBetSchema, CreatedBetResponseSchema, GetBetsSchema
from services.bet_services import BetService

router = APIRouter()


@router.post("/bet/", response_model=CreatedBetResponseSchema)
async def make_bet(
    bet: CreateBetSchema,
    db: AsyncSession = Depends(get_db),
    bet_service: BetService = Depends(),
):
    return await bet_service.create_new_bet(db, bet)


@router.get("/bets/", response_model=list[GetBetsSchema])
async def get_bets(
    db: AsyncSession = Depends(get_db), bet_service: BetService = Depends()
):
    return await bet_service.get_all_available_bets(db)
