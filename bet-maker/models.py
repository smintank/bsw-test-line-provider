from sqlalchemy import Column, Integer, String, DATETIME, func, DECIMAL

from database import Base


class Bet(Base):
    __tablename__ = "bet"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    amount = Column(DECIMAL, default=1.0, nullable=False)
    event_id = Column(Integer, index=True)
    status = Column(String)
    timestamp = Column(DATETIME, default=func.now())
