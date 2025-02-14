import logging
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.events import Event
from repositories.evants import EventRepository
from services.line_provider_api_service import LineProviderAPIService

logger = logging.getLogger(__name__)


class EventService:
    @staticmethod
    async def get_or_create_event(db: AsyncSession, event_id: int) -> Event | None:
        event = await EventRepository.get_event(db, event_id)

        if event:
            now = datetime.now()
            if event.deadline > now + timedelta(seconds=3):
                return event
            if event.deadline < now - timedelta(seconds=3):
                raise HTTPException(
                    status_code=404,
                    detail={"message": "Уже нельзя сделать ставку на это событие."}
                )

        event_data = await LineProviderAPIService.fetch_event(event_id)
        if not event_data:
            logger.debug(f"Событие %s не найдено в Line-provider", event_id)
            return None

        event = Event(
            id=event_data.event_id,
            coefficient=event_data.coefficient,
            deadline=event_data.deadline,
            status=event_data.status,
        )
        return await EventRepository.create_event(db, event)
