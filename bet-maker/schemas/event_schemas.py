from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, condecimal, field_serializer
from models.events import EventStatus


class EventSchema(BaseModel):
    event_id: int
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    deadline: datetime
    status: EventStatus

    @field_serializer("coefficient")
    def serialize_coefficient(self, value: Decimal) -> float:
        return float(value)
