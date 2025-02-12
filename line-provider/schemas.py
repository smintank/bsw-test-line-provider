import enum
from decimal import Decimal

from pydantic import BaseModel


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class SEvent(BaseModel):
    event_id: str
    coefficient: Decimal
    deadline: int
    state: EventState = EventState.NEW
