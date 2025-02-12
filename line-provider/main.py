import decimal
import enum
import time
from decimal import Decimal
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(BaseModel):
    event_id: str
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = EventState.NEW


events: dict[str, Event] = {
    '1': Event(event_id='1', coefficient=Decimal('1.2'), deadline=int(time.time()) + 600),
    '2': Event(event_id='2', coefficient=Decimal('1.15'), deadline=int(time.time()) + 60),
    '3': Event(event_id='3', coefficient=Decimal('1.67'), deadline=int(time.time()) + 90)
}

app = FastAPI()


@app.put('/event')
async def create_event(event: Event):
    if event.event_id not in events:
        events[event.event_id] = event
        return {}

    for p_name, p_value in event.model_dump(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)

    return {}


@app.get('/event/{event_id}')
async def get_event(event_id: str):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


@app.get('/events')
async def get_events():
    return list(e for e in events.values() if time.time() < e.deadline)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)