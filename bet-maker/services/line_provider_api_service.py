import logging

from httpx import AsyncClient, HTTPStatusError, RequestError, DecodingError

from config import settings
from models.events import EventStatus
from schemas.event_schemas import EventSchema
from typing import Optional, List

logger = logging.getLogger(__name__)



class LineProviderAPIService:
    BASE_URL = settings.event_app_url

    STATE_MAPPING = {
        1: EventStatus.NOT_FINISHED.value,
        2: EventStatus.WIN.value,
        3: EventStatus.LOSE.value,
    }

    _client: Optional[AsyncClient] = None

    @classmethod
    def get_client(cls) -> AsyncClient:
        if cls._client is None:
            cls._client = AsyncClient()
        return cls._client

    @classmethod
    async def get_url_data(cls, url: str) -> dict:
        client = cls.get_client()
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except DecodingError as e:
            logger.error("[%s] Ошибка декодирования JSON: %s", url, e)
        except HTTPStatusError as e:
            logger.error("[%s] Ошибка HTTP: %s", url, e)
        except RequestError as e:
            logger.error("[%s] Ошибка запроса: %s", url, e)
        except Exception as e:
            logger.error("[%s] Непредвиденная ошибка: %s", url, e)
        return {}

    @classmethod
    async def fetch_event(cls, event_id: int) -> Optional[EventSchema]:
        data = await cls.get_url_data(f"{cls.BASE_URL}{event_id}/")

        if not data:
            return None

        # Преобразуем status, если он числовой
        if isinstance(data.get("status"), int):
            status_mapping = {
                1: EventStatus.NOT_FINISHED.value,
                2: EventStatus.WIN.value,
                3: EventStatus.LOSE.value
            }
            data["status"] = status_mapping.get(data["status"], EventStatus.NOT_FINISHED.value)

        return EventSchema(**data)

    @classmethod
    async def fetch_available_events(cls) -> List[EventSchema]:
        data = await cls.get_url_data(cls.BASE_URL)
        return [
            EventSchema(
                **{**event, "status": cls.STATE_MAPPING.get(event["status"], EventStatus.NOT_FINISHED.value)}
            )
            for event in data
        ] if data else []

    @classmethod
    async def close_client(cls) -> None:
        if cls._client:
            await cls._client.aclose()
            cls._client = None