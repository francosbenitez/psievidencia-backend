# Generated by Django 4.0.4 on 2022-09-28 16:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_delete_psychologist'),
    ]

    operations = [
        migrations.AddField(
            model_name='authenticated',
            name='additional_data',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='authenticated',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='authenticated',
            name='gender_identity',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='authenticated',
            name='name',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='authenticated',
            name='phone_number',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
