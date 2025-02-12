from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from crud import get_all_bets, create_bet
from schemas import SCreateBet


router = APIRouter(tags=["Bets"])


@router.post("/bet/")
async def make_bet(bet: SCreateBet, db: AsyncSession = Depends(get_db)):
    bet_id = await create_bet(db, bet)
    return {"bet_id": bet_id}


@router.get("/bets/")
async def get_bets(db: AsyncSession = Depends(get_db)):
    bets = await get_all_bets(db)
    return {"bets": bets}