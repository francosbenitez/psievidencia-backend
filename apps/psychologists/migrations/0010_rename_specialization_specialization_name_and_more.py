# Generated by Django 4.0.4 on 2022-06-29 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("psychologists", "0009_therapeuticmodel"),
    ]

    operations = [
        migrations.RenameField(
            model_name="specialization",
            old_name="specialization",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="therapeuticmodel",
            old_name="therapeutic_model",
            new_name="name",
        ),
    ]