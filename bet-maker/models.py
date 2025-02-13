import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, Integer, DECIMAL, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class EventStatus(enum.Enum):
    NOT_FINISHED = 1
    WIN = 2
    LOSE = 3

class Bet(Base):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    coefficient: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
