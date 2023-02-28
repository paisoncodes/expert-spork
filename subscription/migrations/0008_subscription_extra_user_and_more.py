# Generated by Django 4.1.3 on 2023-02-27 19:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0007_alter_subscription_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="extra_user",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 27, 19, 52, 56, 766457)
            ),
        ),
    ]