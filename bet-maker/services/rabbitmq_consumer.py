import asyncio
import json
import logging

import aio_pika

from config import settings
from constants import EVENT_STATUS_MAPPING
from db.session import get_db
from messages import (
    RABBITMQ_EVENT_NOT_UPDATED,
    RABBITMQ_EVENT_UPDATED,
    RABBITMQ_READY_FOR_MSGS,
    RABBITMQ_RUN_CONSUMER,
)
from models.events import EventStatus
from repositories.evants import EventRepository

logger = logging.getLogger(__name__)


async def process_message(message: aio_pika.IncomingMessage):
    """Обрабатывает входящее сообщение RabbitMQ."""
    async with message.process():
        data = json.loads(message.body)
        event_id = data.get("event_id")
        status = data.get("status")

        if event_id and status:
            logger.debug(RABBITMQ_EVENT_UPDATED, event_id, status)

            async for db in get_db():
                enum_status = EVENT_STATUS_MAPPING.get(status, EventStatus.NOT_FINISHED)
                updated_event = await EventRepository.update(
                    db, event_id, status=enum_status
                )
                if not updated_event:
                    logger.warning(RABBITMQ_EVENT_NOT_UPDATED, event_id, status)


async def start_rabbitmq_consumer():
    logger.info(RABBITMQ_RUN_CONSUMER)

    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.rabbitmq_queue, durable=True)
        logger.info(RABBITMQ_READY_FOR_MSGS)

        await queue.consume(lambda msg: asyncio.create_task(process_message(msg)))

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_rabbitmq_consumer())
