# Generated by Django 4.0.4 on 2022-07-12 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psychologists', '0012_education'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenderPerspective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_perspective', models.CharField(default='', max_length=1000)),
                ('psychologists', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gender_perspectives', to='psychologists.psychologist')),
            ],
        ),
    ]