from django.db.models import Manager, Q


class ChatRoomManager(Manager):
    def latest_message(self):
        return self.chat_message_set.latest("sent")


class ChatMessageManager(Manager):
    def between_two_users(self, first_user, second_user):
        return self.filter(
            Q(sender_id=first_user.pk, receiver_id=second_user.pk)
            | Q(sender_id=second_user.pk, receiver_id=first_user.pk)
        )
