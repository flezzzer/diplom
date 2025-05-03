import aiormq
import json
import asyncio
from typing import Any

# Конфигурация RabbitMQ
RABBITMQ_HOST = 'localhost'  # или ваш адрес RabbitMQ
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_VHOST = '/'
RABBITMQ_QUEUE = 'notifications'

# Установить подключение к RabbitMQ
async def get_rabbitmq_connection() -> aiormq.Connection:
    credentials = aiormq.credentials.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = await aiormq.connect(
        f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}',
        loop=asyncio.get_event_loop()
    )
    return connection

# Создать канал для отправки сообщений
async def get_channel() -> aiormq.Channel:
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    return channel

# Создание очереди для уведомлений
async def create_notification_queue(channel: aiormq.Channel) -> None:
    await channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# Отправить уведомление в очередь
async def send_notification(channel: aiormq.Channel, message: dict) -> None:
    await channel.basic_publish(
        json.dumps(message).encode(),  # Преобразуем сообщение в JSON
        routing_key=RABBITMQ_QUEUE,
        delivery_mode=2  # Сделаем сообщение устойчивым
    )
    print("Notification sent:", message)

# Получить уведомления из очереди
async def receive_notifications(channel: aiormq.Channel) -> None:
    await channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=handle_message,
        auto_ack=True
    )

# Обработчик сообщений
async def handle_message(channel: aiormq.Channel, body: bytes, envelope: aiormq.spec.Basic.Deliver, properties: aiormq.spec.Basic.Properties) -> None:
    message = json.loads(body.decode())
    print("Received notification:", message)
    # Здесь вы можете обработать уведомление, например, отправить через WebSocket или в другое место.
