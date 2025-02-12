import time

from fastapi import APIRouter, HTTPException
from schemas import SEvent
from database import events

router = APIRouter(prefix='/events', tags=['Events'])


@router.put('/')
async def create_event(event: SEvent):
    if event.event_id not in events:
        events[event.event_id] = event
        return {}

    for p_name, p_value in event.model_dump(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)

    return {}


@router.get('/')
async def get_events():
    return list(e for e in events.values() if time.time() < e.deadline)


@router.get('/{event_id}')
async def get_event(event_id: str):
    if event_id in events:
        return events[event_id]
    raise HTTPException(status_code=404, detail="Event not found")