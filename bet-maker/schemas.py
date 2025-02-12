import enum

from pydantic import BaseModel, Field, condecimal


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class SBet(BaseModel):
    bet_id: int
    amount: float
    status: EventState


class SCreateBet(BaseModel):
    event_id: int
    amount: condecimal(gt=0, max_digits=20, decimal_places=2)


class SEvent(BaseModel):
    event_id: int
    coefficient: float
    deadline: int
    status: EventState
