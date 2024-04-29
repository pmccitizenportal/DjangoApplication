# Generated by Django 5.0.4 on 2024-04-23 04:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0007_remove_propertytaxapplicationformhistory_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertytaxpropertydetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL),
        ),
    ]