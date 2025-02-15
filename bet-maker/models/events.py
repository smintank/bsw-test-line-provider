from __future__ import annotations

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base


class EventStatus(enum.Enum):
    NOT_FINISHED = "not_finished"
    WIN = "win"
    LOSE = "lose"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    coefficient: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), default=EventStatus.NOT_FINISHED, nullable=False)

    bets: Mapped[list["Bet"]] = relationship("Bet", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event(id={self.id}, coefficient={self.coefficient}, status={self.status.value})>"
