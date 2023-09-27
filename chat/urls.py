from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatIndexView.as_view(), name="index"),
    path(
        "room/create/<int:target_user_pk>",
        views.ChatRoomCreateView.as_view(),
        name="create_room",
    ),
    path("private/<int:room_pk>/", views.ChatRoomView.as_view(), name="room"),
]
