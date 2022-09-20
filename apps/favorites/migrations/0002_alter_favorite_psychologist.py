# Generated by Django 4.0.4 on 2022-09-20 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_psychologistprofile_user_delete_psychologist_and_more'),
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Favorite',
            name='psychologist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='psychologist', to='users.psychologist'),
        ),
    ]
