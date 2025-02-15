from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base


class Bet(Base):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), index=True, nullable=False)
    coefficient: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now(), server_default=func.now())

    event: Mapped["Event"] = relationship("Event", back_populates="bets")

    def __repr__(self):
        return f"<Bet(id={self.id}, amount={self.amount}, event_id={self.event_id}, status={self.event.status.value})>"
