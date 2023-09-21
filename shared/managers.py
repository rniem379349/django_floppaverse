from django.db.models import QuerySet


class PseudoDeleteQuerySet(QuerySet):
    def non_deleted(self):
        return self.filter(deleted_timestamp__isnull=True)

    def deleted(self):
        return self.filter(deleted_timestamp__isnull=False)
