# Generated by Django 5.0.4 on 2024-04-15 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0009_alter_customuser_address_alter_customuser_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='employment_type',
            field=models.CharField(default=None, help_text='Enter your employment type.', max_length=50, null=True),
        ),
    ]
