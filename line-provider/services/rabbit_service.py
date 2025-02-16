import aio_pika
import json

from config import settings


async def send_event_update(event_id: int, status: int):
    """Асинхронно отправляет обновление события в RabbitMQ."""
    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"event_id": event_id, "status": status}).encode()),
            routing_key=settings.rabbitmq_queue
        )
