from django.urls import path

from users.views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserListView,
    UserProfileDetailView,
    UserReportView,
    UserUpdateView,
)

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("list", UserListView.as_view(), name="user_list"),
    path("profile/<int:user_pk>", UserProfileDetailView.as_view(), name="profile"),
    path("profile/<int:user_pk>/edit", UserUpdateView.as_view(), name="profile-edit"),
    path("<int:user_pk>/report", UserReportView.as_view(), name="user-report"),
]
