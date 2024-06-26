# Generated by Django 5.0.4 on 2024-05-02 05:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_360', '0023_alter_pbprojects_submission_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbprojects',
            name='assigned_officer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='assigned_officer_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='beneficiary',
            field=models.CharField(blank=True, choices=[('citizen', 'Citizen'), ('student', 'Student'), ('slum', 'Low-Income Strata')], null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='cost_estimate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal_360.pbcostestimate'),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal_360.department'),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='gis_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal_360.gis'),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='project_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal_360.pbprojectcategory'),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='project_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='submission_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='supporting_documents',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='total_votes_received',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pbprojects',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal_360.ward'),
        ),
    ]
