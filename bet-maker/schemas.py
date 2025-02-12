import enum

from pydantic import BaseModel


class SBet(BaseModel):
    bet_id: int
    amount: float
    status: int


class SCreateBet(BaseModel):
    event_id: int
    amount: float


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class SEvent(BaseModel):
    event_id: int
    coefficient: float
    deadline: int
    status: EventState