"""floppaverse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from floppaverse.views import HomePageRedirectView

urlpatterns = [
    path("", HomePageRedirectView.as_view()),
    path("admin/", admin.site.urls),
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
    path("chat/", include(("chat.urls", "chat"), namespace="chat")),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("django_prometheus.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
