import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.events import Event, EventStatus

logger = logging.getLogger(__name__)


class EventRepository:
    @staticmethod
    async def create_event(db: AsyncSession, event: Event) -> Event:
        """Создает новое событие в БД."""
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

    @staticmethod
    async def get_event(db: AsyncSession, event_id: int) -> Event | None:
        """Возвращает событие по id если оно есть в БД"""
        result = await db.execute(select(Event).filter(Event.id == event_id))
        return result.scalars().first()

    @staticmethod
    async def update_event_status(db: AsyncSession, event_id: int, status: EventStatus) -> Event | None:
        """Обновляет статус всех ставок, связанных с данным событием."""
        event = await EventRepository.get_event(db, event_id)
        if not event:
            return None
        event.status = status
        await db.commit()
        await db.refresh(event)
        return event
