from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatIndexView.as_view(), name="index"),
    path("private/<int:target_user_pk>/", views.ChatRoomView.as_view(), name="room"),
]
