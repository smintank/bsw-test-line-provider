from fastapi import APIRouter, Depends

from schemas.event_schemas import EventSchema
from services.event_services import EventService

router = APIRouter()


@router.get("/", response_model=list[EventSchema])
async def get_available_events(event_service: EventService = Depends()):
    return await event_service.get_all_events()
