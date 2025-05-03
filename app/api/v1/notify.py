from app.core.rabbitmq import get_channel, send_notification, receive_notifications
from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter()

async def notify_seller(seller_id: str, message: str):
    channel = await get_channel()
    notification = {
        'seller_id': seller_id,
        'message': message,
        'type': 'notification'
    }
    await send_notification(channel, notification)

async def start_receiving_notifications():
    channel = await get_channel()
    await receive_notifications(channel)


@router.get("/{seller_id}/send_notification")
async def send_notification_to_seller(seller_id: str):
    # Генерация уведомления (можно добавлять что-то более динамическое)
    message = "У вас новый заказ!"
    await notify_seller(seller_id, message)
    return {"status": "Notification sent"}

active_connections = {}

@router.websocket("/ws/{seller_id}")
async def websocket_endpoint(websocket: WebSocket, seller_id: str):
    await websocket.accept()
    active_connections[seller_id] = websocket

    try:
        while True:
            # Здесь можно обработать уведомления и отправить их через WebSocket
            # Например, уведомление приходит через RabbitMQ и отправляется сюда
            pass
    except WebSocketDisconnect:
        del active_connections[seller_id]