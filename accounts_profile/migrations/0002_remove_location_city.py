# Generated by Django 4.1.3 on 2023-02-15 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts_profile", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="city",
        ),
    ]
