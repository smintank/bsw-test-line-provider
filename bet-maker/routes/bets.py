from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from repositories.bets import BetRepository
from schemas.bet_schemas import CreateBetSchema, GetBetsSchema, CreatedBetResponseSchema
from services.bet_services import BetService
from services.event_services import LineProviderService

router = APIRouter()


@router.post("/bet/", response_model=CreatedBetResponseSchema)
async def make_bet(bet: CreateBetSchema, db: AsyncSession = Depends(get_db)):
    event_data = await LineProviderService.fetch_event(bet.event_id)

    if not event_data:
        raise HTTPException(status_code=404, detail={"message": "Событие не найдено"})

    bet_data = bet.model_dump()
    bet_data["coefficient"] = event_data.coefficient
    bet_data["status"] = event_data.status

    bet_id = await BetService.create_new_bet(db, bet_data)
    return {"bet_id": bet_id}


@router.get("/bets/", response_model=list[GetBetsSchema])
async def get_bets(db: AsyncSession = Depends(get_db)):
    bets = await BetRepository.get_all_bets(db)
    return [GetBetsSchema.model_validate(bet) for bet in bets]
