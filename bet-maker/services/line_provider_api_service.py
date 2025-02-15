import logging

from httpx import AsyncClient, HTTPStatusError, RequestError, DecodingError

from config import settings
from schemas.event_schemas import EventSchema
from typing import Optional, List

logger = logging.getLogger(__name__)


class LineProviderAPIService:
    BASE_URL = settings.event_app_url

    @classmethod
    async def get_url_data(cls, url: str) -> dict | None:
        async with AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except DecodingError as e:
                logger.debug("[%s] Ошибка декодирования JSON: %s", url, e)
            except HTTPStatusError as e:
                logger.error("[%s] Ошибка HTTP: %s", url, e)
            except RequestError as e:
                logger.warning("[%s] Ошибка запроса: %s", url, e)
            except Exception as e:
                logger.exception("[%s] Непредвиденная ошибка: %s", url, e)
            return None

    @classmethod
    async def fetch_event(cls, event_id: int) -> Optional[EventSchema] | None:
        event = await cls.get_url_data(f"{cls.BASE_URL}{event_id}/")
        return EventSchema.model_validate(event) if event else None

    @classmethod
    async def fetch_available_events(cls) -> List[EventSchema]:
        events = await cls.get_url_data(cls.BASE_URL)
        return [EventSchema.model_validate(event) for event in events] if events else []