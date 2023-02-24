# Generated by Django 4.1.3 on 2023-02-24 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Emails",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("receiver", models.CharField(max_length=20)),
                ("message", models.TextField(default="")),
                ("sent", models.BooleanField(default=False)),
                (
                    "response_message",
                    models.CharField(blank=True, max_length=525, null=True),
                ),
                ("status_code", models.CharField(max_length=225)),
                ("subject", models.CharField(default="", max_length=225)),
                ("email", models.EmailField(max_length=254)),
            ],
            options={
                "verbose_name_plural": "Emails",
            },
        ),
        migrations.CreateModel(
            name="Messages",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("receiver", models.CharField(max_length=20)),
                ("message", models.TextField(default="")),
                ("sent", models.BooleanField(default=False)),
                ("response_message", models.CharField(max_length=525)),
                ("message_id", models.CharField(max_length=225)),
                ("email", models.EmailField(max_length=254)),
            ],
            options={
                "verbose_name_plural": "Messages",
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("title", models.CharField(max_length=225)),
                ("object_id", models.CharField(max_length=225)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
