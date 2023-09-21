from django.db import models
from django.db.models.deletion import SET_NULL


class AuthorPseudoDeleteMixin(models.Model):
    author = models.ForeignKey("auth.User", null=True, on_delete=SET_NULL)
    created_timestamp = models.DateTimeField("Created at", auto_now_add=True)
    updated_timestamp = models.DateTimeField("Last updated at", auto_now=True)
    deleted_timestamp = models.DateTimeField("Deleted at", null=True, default=None)

    class Meta:
        abstract = True
