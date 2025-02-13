from decimal import Decimal
from datetime import datetime, timedelta

from schemas import GetEventSchema


events: dict[int, GetEventSchema] = {
    1: GetEventSchema(coefficient=Decimal('1.2'), deadline=datetime.now() + timedelta(hours=1)),
    2: GetEventSchema(coefficient=Decimal('1.15'), deadline=datetime.now() + timedelta(minutes=5)),
    3: GetEventSchema(coefficient=Decimal('1.67'), deadline=datetime.now() + timedelta(minutes=10)),
}
