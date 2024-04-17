# Generated by Django 5.0.4 on 2024-04-17 04:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0013_applicationusage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('bill_date', models.DateField()),
                ('due_date', models.DateField()),
                ('bill_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('penalty', models.DecimalField(decimal_places=2, max_digits=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'water_billing_system_billing',
            },
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('meter_id', models.AutoField(primary_key=True, serialize=False)),
                ('installation_date', models.DateField()),
                ('location', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('connection_status', models.CharField(max_length=100)),
                ('meter_size', models.CharField(max_length=100)),
                ('ae_name', models.CharField(max_length=100)),
                ('je_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'water_billing_system_meter',
            },
        ),
        migrations.CreateModel(
            name='MeterService',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_date', models.DateField()),
                ('service_type', models.CharField(choices=[('installation', 'Installation'), ('repair', 'Repair'), ('maintenance', 'Maintenance')], max_length=20)),
                ('service_details', models.TextField()),
                ('service_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='portal_360.meter')),
            ],
            options={
                'db_table': 'water_billing_system_meter_service',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_date', models.DateField()),
                ('trans_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('online', 'Online')], max_length=20)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='portal_360.billing')),
            ],
            options={
                'db_table': 'water_billing_system_payment',
            },
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('reading_id', models.AutoField(primary_key=True, serialize=False)),
                ('reading_date', models.DateField()),
                ('reading_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reader_name', models.CharField(max_length=100)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='portal_360.meter')),
            ],
            options={
                'db_table': 'water_billing_system_meter_reading',
            },
        ),
    ]
