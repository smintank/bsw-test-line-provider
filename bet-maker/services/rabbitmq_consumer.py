import asyncio
import logging

import pika
import json

from config import settings
from constants import EVENT_STATUS_MAPPING
from db.session import get_db
from messages import RABBITMQ_EVENT_UPDATED, RABBITMQ_EVENT_NOT_UPDATED, RABBITMQ_READY_FOR_MSGS, RABBITMQ_RUN_CONSUMER
from models.events import EventStatus
from repositories.evants import EventRepository

logger = logging.getLogger(__name__)


def process_message(ch, method, properties, body):
    data = json.loads(body)
    event_id = data.get("event_id")
    status = data.get("status")

    if event_id and status:
        logger.debug(RABBITMQ_EVENT_UPDATED, event_id, status)

        async def update_db():
            async for db in get_db():
                enum_status = EVENT_STATUS_MAPPING.get(status, EventStatus.NOT_FINISHED)
                updated_event = await EventRepository.update_event_status(db, event_id, enum_status)
                if not updated_event:
                    logger.warning(RABBITMQ_EVENT_NOT_UPDATED,event_id, status)
        asyncio.run(update_db())

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_rabbitmq_consumer():
    logger.info(RABBITMQ_RUN_CONSUMER)
    credentials = pika.PlainCredentials(settings.rabbitmq_user, settings.rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.rabbitmq_host, port=settings.rabbitmq_port, credentials=credentials
    ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)
    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=process_message)

    logger.info(RABBITMQ_READY_FOR_MSGS)
    channel.start_consuming()


if __name__ == "__main__":
    start_rabbitmq_consumer()