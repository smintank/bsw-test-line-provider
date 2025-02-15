from fastapi import APIRouter

from schemas.event_schemas import EventSchema
from services.event_services import LineProviderAPIService

router = APIRouter()


@router.get("/", response_model=list[EventSchema])
async def get_available_events():
    return await LineProviderAPIService.fetch_available_events()
