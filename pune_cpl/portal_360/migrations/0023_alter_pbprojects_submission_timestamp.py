# Generated by Django 5.0.4 on 2024-05-02 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0022_alter_pbvoting_project_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbprojects',
            name='submission_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]