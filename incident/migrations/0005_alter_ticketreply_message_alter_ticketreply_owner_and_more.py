# Generated by Django 4.1.3 on 2023-02-24 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("incident", "0004_alter_ticket_message_alter_ticket_owner_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketreply",
            name="message",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="ticketreply",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="ticketreply",
            name="ticket",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="incident.ticket",
            ),
        ),
    ]