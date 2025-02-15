import logging
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from messages import EVENT_NOT_IN_API, EVENT_UNAVAILABLE
from models.events import Event
from repositories.evants import EventRepository
from services.line_provider_api_service import LineProviderAPIService

logger = logging.getLogger(__name__)


class EventService:
    @staticmethod
    async def get_or_fetch_event(db: AsyncSession, event_id: int) -> Event | None:
        """Возвращает событие из базы если оно существует или запрашивает по API"""
        if event_from_db := await EventRepository.get_event(db, event_id):
            if event_from_db.deadline >= datetime.now():
                return event_from_db
            else:
                raise HTTPException(status_code=404, detail={"message": EVENT_UNAVAILABLE})

        if event_from_api := await LineProviderAPIService.fetch_event(event_id):
            event_data = event_from_api.model_dump(exclude_unset=True)
            event_data["id"] = event_data.pop("event_id")
            event = Event(**event_data)
            return await EventRepository.create_event(db, event)

        logger.debug(EVENT_NOT_IN_API, event_id)
