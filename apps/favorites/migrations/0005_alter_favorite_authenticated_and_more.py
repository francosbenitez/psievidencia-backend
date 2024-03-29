# Generated by Django 4.0.4 on 2022-09-20 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_psychologist_date"),
        ("favorites", "0004_alter_favorite_authenticated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="authenticated",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorites",
                to="users.authenticated",
            ),
        ),
        migrations.AlterField(
            model_name="favorite",
            name="psychologist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorites",
                to="users.psychologist",
            ),
        ),
    ]
