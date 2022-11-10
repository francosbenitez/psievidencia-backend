# Generated by Django 4.0.4 on 2022-10-10 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("psychologists", "0024_remove_psychologist_specialization_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="psychologist",
            name="province",
        ),
        migrations.AlterField(
            model_name="province",
            name="psychologists",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="province",
                to="psychologists.psychologist",
            ),
        ),
    ]
