# Generated by Django 5.0.4 on 2024-04-12 08:25

import portal_360.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0002_remove_customuser_username_customuser_citizen_id'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', portal_360.models.CustomUserManager()),
            ],
        ),
    ]
