from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from chat.models import ChatMessage, ChatRoom


class ChatIndexView(LoginRequiredMixin, generic.ListView):
    template_name = "chat/index.html"
    model_name = ChatRoom
    context_object_name = "user_rooms"

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "Chat": reverse("chat:index"),
        }

    def get_queryset(self):
        qs = ChatRoom.objects.filter(participants=self.request.user)
        for room in qs:
            other_participants = room.participants.exclude(pk=self.request.user.pk)
            room.other_participants = other_participants
            other_participants_str = ", ".join([u.username for u in other_participants])
            room.other_participants_str = other_participants_str
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.breadcrumbs
        context["site_title"] = "Chat"
        return context


class ChatRoomView(LoginRequiredMixin, generic.TemplateView):
    template_name = "chat/room.html"

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "Chat": reverse("chat:index"),
            "Chat Room": reverse(
                "chat:room",
                kwargs={"target_user_pk": self.kwargs.get("target_user_pk")},
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user_pk = self.kwargs.get("target_user_pk")
        target_user = User.objects.get(pk=target_user_pk)
        context["breadcrumbs"] = self.breadcrumbs
        context["target_user"] = target_user
        context["previous_messages"] = (
            ChatMessage.objects.between_two_users(self.request.user, target_user)
            .select_related("sender", "receiver")
            .order_by("sent")
        )
        return context
