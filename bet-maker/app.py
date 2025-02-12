import uvicorn
from fastapi import FastAPI

from schemas import SCreateBet
from crud import create_bet, get_all_bets, fetch_all_events

app = FastAPI()


@app.get("/events/")
async def get_events():
    return await fetch_all_events()


@app.post("/bet/")
async def make_bet(bet: SCreateBet):
    bet_id = await create_bet(bet)
    return {"bet_id": bet_id}


@app.get("/bets/")
async def get_bets():
    bets = await get_all_bets()
    return {"bets": bets}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
