# Generated by Django 5.0.4 on 2024-04-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0014_alter_cmscomplaints_expected_completion_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmscomplaints',
            name='status',
            field=models.CharField(db_column='status', default='Pending', max_length=50),
        ),
    ]
