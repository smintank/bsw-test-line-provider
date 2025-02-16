import logging
from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from messages import EVENT_NOT_IN_API, EVENT_UNAVAILABLE
from models.events import Event
from repositories.evants import EventRepository
from schemas.event_schemas import EventSchema
from services.line_provider_api_service import LineProviderAPIService

logger = logging.getLogger(__name__)


class EventService:
    def __init__(
        self,
        event_repo: EventRepository = Depends(),
        api_service: LineProviderAPIService = Depends(),
    ):
        self.event_repo = event_repo
        self.api_service = api_service

    async def get_or_fetch_event(self, db: AsyncSession, event_id: int) -> Event | None:
        """Возвращает событие из базы если оно существует или запрашивает по API"""
        if event_from_db := await self.event_repo.get_one(db, event_id):
            if event_from_db.deadline >= datetime.now():
                return event_from_db
            else:
                raise HTTPException(
                    status_code=404, detail={"message": EVENT_UNAVAILABLE}
                )

        if event_from_api := await self.api_service.fetch_event(event_id):
            event_data = event_from_api.model_dump(exclude_unset=True)
            event_data["id"] = event_data.pop("event_id")
            event = Event(**event_data)
            return await self.event_repo.create(db, event)

        logger.debug(EVENT_NOT_IN_API, event_id)

    async def get_all_events(self) -> list[EventSchema]:
        """Запрашивает данные по API и возвращает"""
        return await self.api_service.fetch_available_events()
