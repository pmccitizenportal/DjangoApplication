# Generated by Django 5.0.4 on 2024-04-30 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0017_pbcostestimate_pbprojectcategory_pbprojects_pbbudget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbprojects',
            name='cost_estimate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_360.pbcostestimate'),
        ),
    ]
