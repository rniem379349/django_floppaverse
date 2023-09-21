from django.urls import path

from blog.views import (
    HomeView,
    NewsletterSubscriptionCreateView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostUpdateView,
    SearchResultsView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/<int:blog_post_pk>", PostDetailView.as_view(), name="blog_post_detail"),
    path("post/new", PostCreateView.as_view(), name="blog_post_create"),
    path(
        "post/<int:blog_post_pk>/edit",
        PostUpdateView.as_view(),
        name="blog_post_update",
    ),
    path(
        "post/<int:blog_post_pk>/delete",
        PostDeleteView.as_view(),
        name="blog_post_delete",
    ),
    path(
        "newsletter",
        NewsletterSubscriptionCreateView.as_view(),
        name="newsletter_subscribe",
    ),
    path("search_results", SearchResultsView.as_view(), name="search_results"),
]
