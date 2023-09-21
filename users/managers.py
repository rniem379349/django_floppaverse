from django.db.models import Count, Manager

from shared.managers import PseudoDeleteQuerySet


class ProfileQuerySet(PseudoDeleteQuerySet):
    def with_post_counts(self):
        return self.annotate(num_posts=Count("user__blogpost"))


class ProfileManager(Manager):
    def with_post_counts(self):
        return self.annotate(num_posts=Count("user__blogpost"))
