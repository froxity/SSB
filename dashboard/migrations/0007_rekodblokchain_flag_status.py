# Generated by Django 4.0.3 on 2022-04-03 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_rekodblokchain_owner_rekodharga_data_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='rekodblokchain',
            name='flag_status',
            field=models.BooleanField(null=True),
        ),
    ]