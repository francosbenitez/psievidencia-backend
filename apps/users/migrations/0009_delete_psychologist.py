# Generated by Django 4.0.4 on 2022-09-22 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0006_alter_favorite_psychologist'),
        ('psychologists', '0023_psychologist_alter_education_psychologists_and_more'),
        ('users', '0008_alter_psychologist_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Psychologist',
        ),
    ]
