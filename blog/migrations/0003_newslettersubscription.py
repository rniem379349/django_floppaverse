# Generated by Django 3.2.11 on 2022-01-16 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_blogpost_content_thumbnail"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsletterSubscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=255, verbose_name="Subscriber Email"),
                ),
            ],
        ),
    ]
