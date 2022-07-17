# Generated by Django 4.0.4 on 2022-07-12 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psychologists', '0013_genderperspective'),
    ]

    operations = [
        migrations.RenameField(
            model_name='psychologist',
            old_name='gender',
            new_name='gender_identity',
        ),
        migrations.CreateModel(
            name='GenderIdentity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender_identity', models.CharField(default='', max_length=1000)),
                ('psychologists', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gender_identities', to='psychologists.psychologist')),
            ],
        ),
    ]