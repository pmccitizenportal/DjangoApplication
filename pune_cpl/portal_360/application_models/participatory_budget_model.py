from django.db import models
from django.conf import settings

from ..models import *

class PBProjectCategory(models.Model):
    project_category_id = models.AutoField(primary_key=True)
    project_category_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pb_project_category_master'
    
    def __str__(self):
        return self.project_category_name

class PBCostEstimate(models.Model):
    cost_estimate_id = models.AutoField(primary_key=True)
    cost_estimate_range = models.CharField(max_length=255)

    class Meta:
        db_table = 'pb_cost_estimate_master'
        
    def __str__(self):
        return self.cost_estimate_range

class PBProjects(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    submission_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    project_category = models.ForeignKey(PBProjectCategory, on_delete=models.CASCADE, null=True, blank=True)
    project_title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True, blank=True)
    cost_estimate = models.ForeignKey(PBCostEstimate, on_delete=models.CASCADE, null=True, blank=True)
    allocated_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    priority_level = models.IntegerField(null=True, blank=True)
    requested_deadline = models.DateField(null=True, blank=True)
    estimated_deadline = models.DateField(null=True, blank=True)
    final_implementation_status = models.CharField(max_length=255, choices=[('application_submitted', 'Application Submitted'), ('approved', 'Approved'), ('completed', 'Completed'), ('ongoing', 'Ongoing'), ('rejected', 'Rejected')])
    officer_remarks = models.TextField(null=True, blank=True)
    completion_timestamp = models.DateTimeField(null=True, blank=True)
    citizen_rating = models.IntegerField(null=True, blank=True)
    citizen_feedback = models.TextField(null=True, blank=True)
    tat = models.IntegerField(null=True, blank=True)
    total_votes_received = models.IntegerField(null=True, blank=True)
    assigned_officer = models.CharField(max_length=255, null=True, blank=True)
    assigned_officer_id = models.IntegerField(null=True, blank=True)
    gis_id = models.ForeignKey(GIS, on_delete=models.CASCADE, null=True, blank=True)
    supporting_documents = models.BooleanField(default=False, null=True, blank=True)
    beneficiary = models.CharField(choices=[('citizen', 'Citizen'), ('student', 'Student'), ('slum', 'Low-Income Strata')], null=True, blank=True)
    
    class Meta:
        db_table = 'pb_project_master'

class PBBudget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(PBProjects, on_delete=models.CASCADE)
    cost_estimate = models.ForeignKey(PBCostEstimate, on_delete=models.CASCADE)
    allocated_budget = models.DecimalField(max_digits=12, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assigned_officer = models.CharField(max_length=255)
    assigned_officer_id = models.IntegerField()
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pb_budget_master'

class PBVoting(models.Model):
    voting_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(PBProjects, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    project_category = models.ForeignKey(PBProjectCategory, on_delete=models.CASCADE)
    vote_timestamp = models.DateTimeField()
    vote_type = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('neutral', 'Neutral')])

    class Meta:
        db_table = 'pb_voting_master'
        

