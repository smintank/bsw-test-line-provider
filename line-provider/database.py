import time
from decimal import Decimal

from schemas import SEvent


events: dict[str, SEvent] = {
    '1': SEvent(event_id='1', coefficient=Decimal('1.2'), deadline=int(time.time()) + 6000),
    '2': SEvent(event_id='2', coefficient=Decimal('1.15'), deadline=int(time.time()) + 6000),
    '3': SEvent(event_id='3', coefficient=Decimal('1.67'), deadline=int(time.time()) + 9000)
}
