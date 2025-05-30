import aiormq
import json
import asyncio
from typing import Any

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_VHOST = '/'
RABBITMQ_QUEUE = 'notifications'

async def get_rabbitmq_connection() -> aiormq.Connection:
    credentials = aiormq.credentials.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = await aiormq.connect(
        f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}',
        loop=asyncio.get_event_loop()
    )
    return connection

async def get_channel() -> aiormq.Channel:
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    return channel

async def create_notification_queue(channel: aiormq.Channel) -> None:
    await channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

async def send_notification(channel: aiormq.Channel, message: dict) -> None:
    await channel.basic_publish(
        json.dumps(message).encode(),
        routing_key=RABBITMQ_QUEUE,
        delivery_mode=2
    )
    print("Notification sent:", message)

async def receive_notifications(channel: aiormq.Channel) -> None:
    await channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=handle_message,
        auto_ack=True
    )

async def handle_message(channel: aiormq.Channel, body: bytes, envelope: aiormq.spec.Basic.Deliver, properties: aiormq.spec.Basic.Properties) -> None:
    message = json.loads(body.decode())
    print("Received notification:", message)
