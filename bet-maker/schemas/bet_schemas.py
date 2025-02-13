from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, condecimal, field_serializer, ConfigDict
from models.bets import EventStatus


class GetBetsSchema(BaseModel):
    id: int
    amount: condecimal(gt=0, max_digits=20, decimal_places=2)
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    status: EventStatus
    event_id: int
    timestamp: datetime

    @field_serializer("amount", "coefficient")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value) if value is not None else 0.0

    model_config = ConfigDict(from_attributes=True)


class CreateBetSchema(BaseModel):
    event_id: int
    amount: condecimal(gt=0, max_digits=20, decimal_places=2)

    model_config = {"extra": "forbid"}


class CreatedBetResponseSchema(BaseModel):
    bet_id: int
