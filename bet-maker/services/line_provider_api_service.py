import logging
from typing import List, Optional

from httpx import AsyncClient, DecodingError, HTTPStatusError, RequestError

from config import settings
from messages import (API_HTTP_ERROR, API_JSON_ERROR, API_REQUEST_ERROR,
                      API_UNKNOWN_ERROR)
from schemas.event_schemas import EventSchema

logger = logging.getLogger(__name__)


class LineProviderAPIService:
    BASE_URL = settings.event_app_url

    @classmethod
    async def get_url_data(cls, url: str) -> dict:
        async with AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except DecodingError as e:
                logger.debug(API_JSON_ERROR, url, e)
            except HTTPStatusError as e:
                logger.error(API_HTTP_ERROR, url, e)
            except RequestError as e:
                logger.warning(API_REQUEST_ERROR, url, e)
            except Exception as e:
                logger.exception(API_UNKNOWN_ERROR, url, e)
            return {}

    @classmethod
    async def fetch_event(cls, event_id: int) -> Optional[EventSchema] | None:
        event = await cls.get_url_data(f"{cls.BASE_URL}{event_id}/")
        return EventSchema.model_validate(event) if event else None

    @classmethod
    async def fetch_available_events(cls) -> List[EventSchema]:
        events = await cls.get_url_data(cls.BASE_URL)
        return [EventSchema.model_validate(event) for event in events] if events else []
