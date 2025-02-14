import pika
import json

from config import settings


def send_event_update(event_id: int, status: int):
    credentials = pika.PlainCredentials(settings.rabbitmq_user, settings.rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.rabbitmq_host, port=settings.rabbitmq_port, credentials=credentials
    ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)

    message = json.dumps({"event_id": event_id, "status": status})
    channel.basic_publish(exchange='', routing_key=settings.rabbitmq_queue, body=message)
    connection.close()