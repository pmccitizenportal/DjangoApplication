from django.db import models
from django.conf import settings
from django.utils.timezone import now

from .master_tables import *
from ..common_data import COMPLAINT_SUBTYPE_CHOICES, COMPLAINT_TYPE_CHOICES

class CMSComplaintType(models.Model):
    complaint_type_id = models.IntegerField(primary_key=True, db_column='complaint_type_id', verbose_name='Complaint Type ID')
    complaint_type = models.CharField(choices=COMPLAINT_TYPE_CHOICES, db_column='complaint_type')

    class Meta:
        db_table = 'cms_complaint_type'

    def __str__(self):
        return self.complaint_type

class CMSComplaintSubType(models.Model):
    complaint_sub_type_id = models.IntegerField(primary_key=True, db_column='complaint_sub_type_id', verbose_name='Complaint Sub Type ID')
    complaint_sub_type = models.CharField(max_length=255, choices=COMPLAINT_SUBTYPE_CHOICES, db_column='complaint_sub_type')
    complaint_type_id = models.ForeignKey(CMSComplaintType, on_delete=models.CASCADE, db_column='complaint_type_id')

    class Meta:
        db_table = 'cms_complaint_subtype'

    def __str__(self):
        return self.complaint_sub_type

class CMSComplaints(models.Model):
    complaint_id = models.AutoField(primary_key=True, db_column='complaint_id', verbose_name='Complaint ID')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    registration_date = models.DateField(db_column='registration_date', default=now)
    expected_completion_date = models.DateField(db_column='expected_completion_date', null=True, blank=True)
    complaint_type_id = models.ForeignKey('CMSComplaintType', on_delete=models.CASCADE, db_column='complaint_type_id')
    complaint_sub_type_id = models.ForeignKey('CMSComplaintSubType', on_delete=models.CASCADE, db_column='complaint_sub_type_id')
    description = models.TextField(db_column='description')
    subject = models.TextField(db_column='subject')
    status = models.CharField(max_length=50, db_column='status', default='Pending')
    completion_date = models.DateField(db_column='completion_date', null=True, blank=True)
    rating = models.IntegerField(db_column='rating', null=True, blank=True)
    attachments = models.FileField(upload_to='attachments/', null=True, blank=True)
    feedback = models.TextField(db_column='feedback', null=True, blank=True)
    reopen = models.BooleanField(db_column='reopen', default=False)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, db_column='ward_id')
    address = models.CharField(max_length=255, db_column='address')
    peth = models.ForeignKey(Peth, on_delete=models.CASCADE, null=True, blank=True)
    gis = models.ForeignKey(GIS, on_delete=models.CASCADE, null=True, blank=True)
    pincode = models.ForeignKey(Pincode, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_id', null=True, blank=True)

    class Meta:
        db_table = 'cms_complaints'

    def __str__(self):
        return f"Complaint ID: {self.complaint_id}"