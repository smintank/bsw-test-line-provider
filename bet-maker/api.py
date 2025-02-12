from fastapi import APIRouter

from crud import fetch_all_events, get_all_bets, create_bet
from schemas import SCreateBet


router = APIRouter()

@router.get("/events/")
async def get_events():
    return await fetch_all_events()


@router.post("/bet/")
async def make_bet(bet: SCreateBet):
    bet_id = await create_bet(bet)
    return {"bet_id": bet_id}


@router.get("/bets/")
async def get_bets():
    bets = await get_all_bets()
    return {"bets": bets}