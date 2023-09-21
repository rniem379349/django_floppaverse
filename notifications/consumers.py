# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    origin_user = target_user = None
    notification_channel_name = "notifications__broadcast"
    chat_notification_channel_name = ""

    async def connect(self):
        self.origin_user = self.scope.get("user", "")
        self.chat_notification_channel_name = f"chat_notifications__{self.origin_user}"

        # Throw out non-authenticated users (added layer of protection,
        # permissions should be handled in django view)
        if not self.origin_user or not self.origin_user.is_authenticated:
            return

        # Join room group
        await self.channel_layer.group_add(
            self.notification_channel_name, self.channel_name
        )
        await self.channel_layer.group_add(
            self.chat_notification_channel_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.notification_channel_name, self.channel_name
        )
        await self.channel_layer.group_discard(
            self.chat_notification_channel_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.notification_channel_name,
            {
                "type": "notification",
                "chat_notification": False,
                "sent": text_data_json["sent"],
                "sender": text_data_json["sender"],
                "sender_pic": text_data_json["sender_pic"],
                "message": message_content,
                "notification_url": text_data_json["notification_url"],
            },
        )
        await self.channel_layer.group_send(
            self.chat_notification_channel_name,
            {
                "type": "notification",
                "chat_notification": True,
                "sent": text_data_json["sent"],
                "sender": text_data_json["sender"],
                "sender_username": text_data_json["sender_username"],
                "sender_pic": text_data_json["sender_pic"],
                "message": message_content,
            },
        )

    # Receive message from room group
    async def notification(self, event):
        message = event.get("message", "")
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "chat_notification": event.get("chat_notification", False),
                    "sent": event.get("sent", ""),
                    "sender": event.get("sender", ""),
                    "sender_pic": event.get("sender_pic", ""),
                    "sender_username": event.get("sender_username", ""),
                    "notification_url": event.get("notification_url", ""),
                }
            )
        )
