# Generated by Django 4.0.4 on 2022-06-09 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "psychologists",
            "0002_psychologist_additional_data_psychologist_city_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Specialization",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("specialization", models.CharField(default="", max_length=1000)),
            ],
        ),
    ]
