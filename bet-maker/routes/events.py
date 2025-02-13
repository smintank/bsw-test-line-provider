from fastapi import APIRouter

from schemas.event_schemas import EventSchema
from services.event_services import LineProviderService


router = APIRouter()

@router.get("/")
async def get_available_events() -> list[EventSchema]:
    return await LineProviderService.fetch_available_events()
