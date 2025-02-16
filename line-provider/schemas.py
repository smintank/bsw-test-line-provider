import enum
from datetime import datetime
from decimal import Decimal
from itertools import count
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    condecimal,
    field_serializer,
    field_validator,
)


class EventStatus(enum.Enum):
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
    status: EventStatus = EventStatus.NEW

    @field_serializer("coefficient")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)

    model_config = ConfigDict(from_attributes=True)


class CreateEventSchema(BaseModel):
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    deadline: datetime

    @field_validator("deadline")
    @classmethod
    def check_naive_datetime(cls, value: datetime):
        """Запрещает datetime с timezone"""
        if value.tzinfo is not None:
            raise ValueError("Datetime must be offset-naive (without timezone)")
        return value


class UpdateEventSchema(BaseModel):
    coefficient: Optional[condecimal(gt=0, max_digits=20, decimal_places=2)] = None
    deadline: Optional[datetime] = None
    status: Optional[EventStatus] = None
