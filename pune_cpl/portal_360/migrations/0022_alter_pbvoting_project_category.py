# Generated by Django 5.0.4 on 2024-04-30 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0021_alter_pbbudget_cost_estimate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbvoting',
            name='project_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_360.pbprojectcategory'),
        ),
    ]
