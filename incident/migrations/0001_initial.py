# Generated by Django 4.1.3 on 2023-02-21 22:25

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts_profile", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IncidentNature",
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
                ("nature", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="IncidentType",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("title", models.CharField(max_length=30)),
                ("message", models.TextField()),
                ("read", models.BooleanField(default=False)),
                ("closed", models.BooleanField(default=False)),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TicketReply",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("message", models.TextField()),
                ("read", models.BooleanField(default=False)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="incident.ticket",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TicketAssignee",
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
                (
                    "assignee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_assignee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="incident.ticket",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Incident",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("name", models.CharField(max_length=225)),
                ("incident_type", models.CharField(max_length=225)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("details", models.TextField()),
                ("past_occurrences", models.JSONField(default=dict)),
                ("number_of_victims", models.IntegerField(default=0)),
                ("special_events", models.TextField()),
                ("prior_warnings", models.TextField()),
                ("perpetrators", models.TextField()),
                ("evidence", models.JSONField(default=dict)),
                ("company_approved", models.BooleanField(default=False)),
                ("admin_approved", models.BooleanField(default=False)),
                (
                    "incident_nature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="incident.incidentnature",
                    ),
                ),
                (
                    "lga",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts_profile.lga",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        default=accounts.models.User.get_default_pk,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts_profile.state",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
