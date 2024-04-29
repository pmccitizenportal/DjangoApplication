# Generated by Django 5.0.4 on 2024-04-22 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0002_alter_propertytaxpropertydetail_verification_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='GIS',
            fields=[
                ('gis_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
            options={
                'db_table': 'gis_master',
            },
        ),
        migrations.CreateModel(
            name='Pincode',
            fields=[
                ('pincode_id', models.AutoField(primary_key=True, serialize=False)),
                ('pincode', models.CharField(max_length=10, unique=True)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('peth', models.TextField()),
                ('ward', models.TextField()),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'pincode_master',
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('ward_id', models.AutoField(primary_key=True, serialize=False)),
                ('ward_name', models.TextField()),
            ],
            options={
                'db_table': 'ward_master',
            },
        ),
        migrations.CreateModel(
            name='Peth',
            fields=[
                ('peth_id', models.AutoField(primary_key=True, serialize=False)),
                ('peth_name', models.TextField()),
                ('ward_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='portal_360.ward')),
            ],
            options={
                'db_table': 'peth_master',
            },
        ),
    ]
