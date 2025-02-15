from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, condecimal, field_serializer, model_validator, ConfigDict

from constants import EVENT_STATUS_MAPPING
from models.events import EventStatus


class EventSchema(BaseModel):
    event_id: int
    coefficient: condecimal(gt=0, max_digits=20, decimal_places=2)
    deadline: datetime
    status: EventStatus

    @field_serializer("coefficient")
    def serialize_coefficient(self, value: Decimal) -> float:
        return float(value)

    @model_validator(mode="before")
    @classmethod
    def convert_status(cls, value: int) -> EventStatus:
        return EVENT_STATUS_MAPPING.get(value, EventStatus.NOT_FINISHED)

    model_config = ConfigDict(from_attributes=True)
