from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, condecimal, field_serializer

from models import EventStatus


class EventSchema(BaseModel):
    event_id: int
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    deadline: datetime
    status: EventStatus = EventStatus.NOT_FINISHED


class GetBetsSchema(BaseModel):
    id: int
    amount: condecimal(gt=0, max_digits=20, decimal_places=2)
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    status: int
    event_id: EventStatus
    timestamp: datetime

    @field_serializer("amount", "coefficient")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)


class CreateBetSchema(BaseModel):
    event_id: int
    amount: condecimal(gt=0, max_digits=20, decimal_places=2)

    model_config = {"extra": "forbid"}


class CreatedBetResponseSchema(BaseModel):
    bet_id: int
