from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views import generic

from chat.models import ChatRoom


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


class ChatRoomCreateView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        target_user = User.objects.get(pk=self.kwargs.get("target_user_pk"))
        room_name = ChatRoom.get_chat_room_name_str([target_user, self.request.user])
        room_exists = ChatRoom.objects.filter(name=room_name).exists()
        if room_exists:
            room = ChatRoom.objects.get(name=room_name)
            return reverse_lazy("chat:room", kwargs={"room_pk": room.pk})
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        room.participants.add(target_user, self.request.user)
        return reverse_lazy("chat:room", kwargs={"room_pk": room.pk})


class ChatRoomView(LoginRequiredMixin, generic.TemplateView):
    template_name = "chat/room.html"

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "Chat": reverse("chat:index"),
            "Chat Room": reverse(
                "chat:room",
                kwargs={"room_pk": self.kwargs.get("room_pk")},
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_pk = self.kwargs.get("room_pk")
        room = ChatRoom.objects.get(pk=room_pk)
        target_user = room.participants.exclude(pk=self.request.user.pk).first()
        context["room"] = room
        context["breadcrumbs"] = self.breadcrumbs
        context["target_user"] = target_user
        context["previous_messages"] = room.has_messages.all().order_by("sent")
        return context
