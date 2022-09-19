# Generated by Django 4.0.4 on 2022-09-19 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('AUTHENTICATED', 'Authenticated'), ('PSYCHOLOGIST', 'Psychologist')], default='', max_length=50),
        ),
    ]
