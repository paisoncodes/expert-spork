# Generated by Django 4.1.3 on 2023-02-24 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("incident", "0003_alter_ticket_message_alter_ticket_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="message",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ticket_owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="title",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]