# Generated by Django 4.0.4 on 2022-09-13 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("psychologists", "0018_alter_psychologist_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="psychologist",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
