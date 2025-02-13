import enum
from datetime import datetime
from decimal import Decimal
from itertools import count
from typing import Optional

from pydantic import BaseModel, Field, condecimal, field_serializer


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


index_generator = count(start=1)

def next_index() -> int:
    return next(index_generator)


class GetEventSchema(BaseModel):
    event_id: int = Field(default_factory=next_index)
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    deadline: datetime
    state: EventState = EventState.NEW

    @field_serializer("coefficient")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)


class CreateEventSchema(BaseModel):
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    deadline: datetime


class UpdateEventSchema(BaseModel):
    coefficient: Optional[condecimal(gt=0, max_digits=20, decimal_places=2)] = None
    deadline: Optional[datetime] = None
    state: Optional[EventState] = None