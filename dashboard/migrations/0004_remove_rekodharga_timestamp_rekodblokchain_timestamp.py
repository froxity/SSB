# Generated by Django 4.0.3 on 2022-03-19 04:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rekodblokchain_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rekodharga',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='rekodblokchain',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
