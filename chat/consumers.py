# chat/consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils import timezone

from chat.models import ChatMessage, ChatRoom
from shared.prometheus import chat_msgs_sent


class ChatConsumer(AsyncWebsocketConsumer):
    origin_user = target_user = None

    @database_sync_to_async
    def get_user_with_profile(self, pk):
        return User.objects.select_related("profile").get(pk=pk)

    @database_sync_to_async
    def save_chat_message(self, message, room_name):
        chat_room = ChatRoom.objects.get_or_create(name=room_name)
        chat_room[0].participants.add(message["sender"], message["receiver"])
        return ChatMessage.objects.create(
            in_chat_room=chat_room[0],
            sender=message["sender"],
            receiver=message["receiver"],
            content=message["content"],
        )

    async def connect(self):
        target_user_pk = self.scope["url_route"]["kwargs"]["target_user_pk"]
        self.origin_user = await self.get_user_with_profile(self.scope.get("user").pk)
        self.target_user = await self.get_user_with_profile(target_user_pk)
        self.target_user_chat_notification_channel_name = (
            f"chat_notifications__{self.target_user}"
        )

        # Throw out non-authenticated users
        # (added layer of protection, permissions should be handled in django view)
        if not self.origin_user or not self.origin_user.is_authenticated:
            return

        self.room_group_name = "chat__" + "__".join(
            sorted((self.origin_user.username, self.target_user.username))
        )
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Alerts users that new user has joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{self.origin_user} has joined the chat.",
            },
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Alerts users that user has left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{self.origin_user} has left the chat.",
            },
        )
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        now = timezone.now()
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]
        message_content_short = (
            message_content[:10] + "..."
            if len(message_content) > 10
            else message_content
        )

        message = {
            "sender": self.origin_user,
            "receiver": self.target_user,
            "content": message_content,
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sent": now.strftime("%b %d, %Y, %H:%M"),
                "sender": self.origin_user.pk,
                "receiver": self.target_user.pk,
                "message": message_content,
            },
        )
        # Send message notification to target user
        await self.channel_layer.group_send(
            self.target_user_chat_notification_channel_name,
            {
                "type": "notification",
                "chat_notification": True,
                "sent": now.strftime("%b %d, %Y, %H:%M"),
                "sender": self.origin_user.pk,
                "sender_username": self.origin_user.username,
                "sender_pic": self.origin_user.profile.profile_pic.url,
                "message": message_content_short,
            },
        )
        # Save message in DB
        await self.save_chat_message(message, self.room_group_name)

    # Receive message from room group
    async def chat_message(self, event):
        message = event.get("message", "")
        sent = event.get("sent", "")
        sender = event.get("sender", "")
        receiver = event.get("receiver", "")
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sent": sent,
                    "sender": sender,
                    "receiver": receiver,
                }
            )
        )
        chat_msgs_sent.inc()
