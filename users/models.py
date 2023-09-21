from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from PIL import Image

from floppaverse.settings import DEFAULT_DATETIME_FORMAT
from shared.mixins.models import AuthorPseudoDeleteMixin
from users.managers import ProfileManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="uploads/profile_pics/%Y/%m/",
        blank=True,
        default="uploads/profile_pics/default.jpg",
    )

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"user_pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_path = self.profile_pic.path
        img = Image.open(img_path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(img_path)

    @property
    def total_posts(self):
        return self.user.blogpost_set.count()

    def latest_posts(self, limit=3):
        if not isinstance(limit, int):
            raise TypeError("limit needs to be an integer.")
        return self.user.blogpost_set.all()[:limit]


class UserReport(AuthorPseudoDeleteMixin, models.Model):
    class ReportTypeChoices(models.TextChoices):
        VULGARITY = "VLG", "Vulgarity"
        VIOLENCE = "VLC", "Violence"
        ABUSE = "ABS", "Abuse"
        OTHER = "OTH", "Other"

    target_user = models.ForeignKey(
        "auth.User",
        verbose_name="Target User",
        related_name="has_user_reports",
        on_delete=models.SET_NULL,
        null=True,
    )
    type = models.CharField(
        "Report type",
        max_length=3,
        choices=ReportTypeChoices.choices,
        default=ReportTypeChoices.OTHER,
        blank=False,
    )
    contact_mail = models.EmailField(
        "Contact Email", max_length=150, default="", blank=True
    )
    content = models.TextField("Content")

    def __str__(self):
        timestamp_str = self.created_timestamp.strftime(DEFAULT_DATETIME_FORMAT)
        return f"{timestamp_str}, against {self.target_user}"
