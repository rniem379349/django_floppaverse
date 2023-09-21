import django_filters
from django.db.models import Count

from users.models import Profile


class NumPostsOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("num_posts", "Number of posts"),
            ("-num_posts", "Number of posts (descending)"),
        ]

    def filter(self, qs, value):
        if value and any(v in ["num_posts"] for v in value):
            return (
                qs.select_related("user")
                .annotate(num_posts=Count("user__blogpost"))
                .order_by("num_posts")
            )
        elif value and any(v in ["-num_posts"] for v in value):
            return (
                qs.select_related("user")
                .annotate(num_posts=Count("user__blogpost"))
                .order_by("-num_posts")
            )

        return super().filter(qs, value)


class ProfileFilter(django_filters.FilterSet):
    order_filter = NumPostsOrderingFilter(
        fields=(("user__username", "user__username"),)
    )

    class Meta:
        model = Profile
        fields = {
            "user__username": ["icontains"],
        }

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related("user").annotate(num_posts=Count("user__blogpost"))
