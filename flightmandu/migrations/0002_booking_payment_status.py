# Generated by Django 4.2 on 2024-05-21 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightmandu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
