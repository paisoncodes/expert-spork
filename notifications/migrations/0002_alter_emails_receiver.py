# Generated by Django 4.1.3 on 2023-02-24 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emails",
            name="receiver",
            field=models.EmailField(max_length=254),
        ),
    ]
