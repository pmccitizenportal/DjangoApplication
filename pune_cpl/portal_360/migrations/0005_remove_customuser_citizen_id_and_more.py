# Generated by Django 5.0.4 on 2024-04-15 07:24

import django.core.validators
import re
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0004_alter_customuser_citizen_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='citizen_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='aadhar_card_id',
            field=models.CharField(default=None, max_length=12, validators=[django.core.validators.RegexValidator(message='Aadhar card number must be 12 digits.', regex='^\\d{12}$')]),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(default=None, help_text='Enter your address.'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='children_details',
            field=models.JSONField(blank=True, default=None, help_text="Enter children's names and ages as JSON.", null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='dob',
            field=models.DateField(default=None, help_text='Enter your date of birth.'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='employment_type',
            field=models.CharField(default=None, help_text='Enter your employment type.', max_length=50),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='customuser',
            name='geographical_details',
            field=models.JSONField(default=None, help_text='Enter geographical details as JSON.'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], default=None, max_length=15),
        ),
        migrations.AddField(
            model_name='customuser',
            name='nationality',
            field=models.CharField(default=None, help_text='Enter your nationality.', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='occupation',
            field=models.CharField(default=None, help_text='Enter your occupation.', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='pan_card_id',
            field=models.CharField(default=None, max_length=10, validators=[django.core.validators.RegexValidator(message="PAN card number must be in the format: 'ABCDE1234F'.", regex='^[A-Z]{5}\\d{4}[A-Z]$')]),
        ),
        migrations.AddField(
            model_name='customuser',
            name='place_of_birth',
            field=models.CharField(default=None, help_text='Enter your place of birth.', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ration_card_id',
            field=models.CharField(default=None, max_length=12, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
        migrations.AddField(
            model_name='customuser',
            name='spouse_name',
            field=models.CharField(blank=True, default=None, help_text="Enter spouse's name if applicable.", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=None, max_length=150, unique=True),
        ),
    ]
