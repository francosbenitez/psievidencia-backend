# Generated by Django 4.0.4 on 2022-06-09 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("psychologists", "0006_rename_psychologistid_specialization_psychologist_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="specialization",
            old_name="psychologist_id",
            new_name="psychologist",
        ),
    ]