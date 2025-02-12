from sqlalchemy import Column, Integer, String, DATETIME, func, DECIMAL

from database import Base


class Bet(Base):
    __tablename__ = "bet"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    amount = Column(DECIMAL, default=1.0, nullable=False)
    event_id = Column(Integer, index=True, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DATETIME, default=func.now())
