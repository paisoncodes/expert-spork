# Generated by Django 4.1.3 on 2023-03-10 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incident", "0007_advisory_alerttype_impact_primarythreatactor_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AffectedGroup",
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
                ("name", models.CharField(max_length=40)),
                ("definition", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="incident",
            name="advisory",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="incident",
            name="affected_groups",
            field=models.ManyToManyField(null=True, to="incident.affectedgroup"),
        ),
    ]
