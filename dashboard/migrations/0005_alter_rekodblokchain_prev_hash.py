# Generated by Django 4.0.3 on 2022-06-14 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_rekodblokchain_data_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rekodblokchain',
            name='prev_hash',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
