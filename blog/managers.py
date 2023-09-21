from shared.managers import PseudoDeleteQuerySet


class BlogPostQuerySet(PseudoDeleteQuerySet):
    def latest_posts(self, limit=3):
        if not isinstance(limit, int):
            raise TypeError("limit needs to be an integer.")
        return self[:limit]
