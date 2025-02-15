from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, condecimal, field_serializer

from schemas.event_schemas import EventSchema


class GetBetsSchema(BaseModel):
    id: int
    amount: condecimal(gt=0, max_digits=20, decimal_places=2)
    event: EventSchema

    @field_serializer("amount")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value) if value is not None else 0.0

    model_config = ConfigDict(from_attributes=True)


class CreateBetSchema(BaseModel):
    event_id: int = Field(gt=0)
    amount: condecimal(gt=0, max_digits=20, decimal_places=2)

    model_config = ConfigDict(extra="forbid")


class CreatedBetResponseSchema(BaseModel):
    bet_id: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)
