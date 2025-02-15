from datetime import datetime

from fastapi import APIRouter, HTTPException, Path


from schemas import GetEventSchema, CreateEventSchema, UpdateEventSchema, EventStatus
from services.rabbit_service import send_event_update
from database import events

router = APIRouter(prefix='/events', tags=['Events'])


@router.post('/', status_code=201)
async def create_event(event: CreateEventSchema) -> GetEventSchema:
    new_event = GetEventSchema(**event.model_dump())
    events[new_event.event_id] = new_event
    return new_event


@router.patch('/{event_id}/', status_code=200, response_model=GetEventSchema)
async def update_event(event: UpdateEventSchema, event_id: int = Path(..., gt=0)):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")

    existing_event = events[event_id]

    updated_data = event.model_dump(exclude_unset=True)
    [setattr(existing_event, key, value) for key, value in updated_data.items()]
    events[event_id] = existing_event
    if "status" in updated_data:
        send_event_update(event_id, existing_event.status.value)

    return existing_event


@router.get('/', status_code=200)
async def get_events() -> list[GetEventSchema]:
    return list(GetEventSchema.model_validate(e) for e in events.values() if datetime.now() < e.deadline)


@router.get('/{event_id}/', status_code=200)
async def get_event(event_id: int = Path(..., gt=0)) -> GetEventSchema:
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return events[event_id]