# Generated by Django 4.1.3 on 2023-03-03 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incident", "0005_alter_ticketreply_message_alter_ticketreply_owner_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="incident",
            name="address",
            field=models.CharField(default=str, max_length=225),
        ),
    ]