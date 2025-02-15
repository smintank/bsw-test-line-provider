from datetime import datetime
from decimal import Decimal

from pydantic import (BaseModel, ConfigDict, condecimal, field_serializer,
                      model_validator)

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
    def convert_status(cls, values: EventStatus | int) -> EventStatus:
        if isinstance(values, dict) and isinstance(values.get("status"), int):
            values["status"] = EVENT_STATUS_MAPPING.get(values["status"], EventStatus.NOT_FINISHED)
        return values

    model_config = ConfigDict(from_attributes=True)
