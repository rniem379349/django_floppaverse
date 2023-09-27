from django.db import models

from chat.managers import ChatMessageManager, ChatRoomManager


class ChatRoom(models.Model):
    name = models.CharField("Room name", max_length=255, unique=True)
    participants = models.ManyToManyField("auth.User", related_name="has_conversations")

    objects = ChatRoomManager()

    @classmethod
    def get_chat_room_name_str(cls, participants):
        return "__".join(sorted([p.username for p in participants]))

    @property
    def latest_message(self):
        return self.has_messages.latest("sent")


class ChatMessage(models.Model):
    in_chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, null=True, related_name="has_messages"
    )
    sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        "auth.User",
        null=False,
        related_name="has_sent_messages",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        "auth.User",
        null=False,
        related_name="has_received_messages",
        on_delete=models.CASCADE,
    )
    content = models.TextField("Content", blank=False)

    objects = ChatMessageManager()

    class Meta:
        ordering = ("-sent",)

    def __str__(self):
        return self.content[:20] + "..." if len(self.content) > 20 else self.content
