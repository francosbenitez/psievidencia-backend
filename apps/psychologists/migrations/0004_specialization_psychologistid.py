# Generated by Django 4.0.4 on 2022-06-09 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("psychologists", "0003_specialization"),
    ]

    operations = [
        migrations.AddField(
            model_name="specialization",
            name="psychologistId",
            field=models.IntegerField(default=0),
        ),
    ]