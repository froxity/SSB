# Generated by Django 4.0.3 on 2022-03-19 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('dashboard', '0002_remove_rekodblokchain_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='rekodblokchain',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
    ]
