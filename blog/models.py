from ckeditor.fields import RichTextField
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from blog.managers import BlogPostQuerySet
from shared.mixins.models import AuthorPseudoDeleteMixin


def get_thumbnail_upload_path(instance, filename):
    return f"uploads/blog_posts/{instance.pk}/images/{filename}"


class BlogPost(AuthorPseudoDeleteMixin, models.Model):
    # author - inherited from AuthorPseudoDeleteMixin
    # created_timestamp - inherited from AuthorPseudoDeleteMixin
    # updated_timestamp - inherited from AuthorPseudoDeleteMixin
    title = models.CharField(verbose_name="Post title", max_length=120, blank=False)
    content = RichTextField(blank=False)
    thumbnail = models.ImageField(upload_to=get_thumbnail_upload_path, blank=True)

    objects = BlogPostQuerySet.as_manager()

    class Meta:
        abstract = False
        ordering = ("-updated_timestamp", "-created_timestamp")

    def get_absolute_url(self):
        return reverse("blog:blog_post_detail", kwargs={"blog_post_pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.thumbnail:
            img = Image.open(self.thumbnail.path)

            output_size = (min(img.width, 1920), min(img.height, 400))
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)

    def __str__(self):
        return "{}, by {}".format(self.title, self.author)

    @property
    def get_thumbnail(self):
        return self.thumbnail.url if self.thumbnail else ""

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def is_recent(self):
        """
        Return True if the post was created less than a day ago.
        """
        now = timezone.now().timestamp()
        return now - self.created_timestamp.timestamp() <= 3600 * 24

    def user_is_author(self, user):
        return user is self.author


class NewsletterSubscription(models.Model):
    email = models.EmailField("Subscriber Email", max_length=255, blank=False)

    def __str__(self):
        return self.email
