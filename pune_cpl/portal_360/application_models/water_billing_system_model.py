from django.db import models
from django.conf import settings

class Meter(models.Model):
    meter_id = models.AutoField(primary_key=True)
    installation_date = models.DateField()
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    connection_status = models.CharField(max_length=100)
    meter_size = models.CharField(max_length=100)
    ae_name = models.CharField(max_length=100)
    je_name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meters')

    def __str__(self):
        return f"Meter {self.meter_id} - {self.user}"
    
    class Meta:
        db_table = 'water_billing_system_meter'
    
class Reading(models.Model):
    reading_id = models.AutoField(primary_key=True)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name='readings')
    reading_date = models.DateField()
    reading_value = models.DecimalField(max_digits=10, decimal_places=2)
    reader_name = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reading {self.reading_id} for Meter {self.meter.meter_id}"
    
    class Meta:
        db_table = 'water_billing_system_meter_reading'

class Billing(models.Model):
    bill_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bills')
    bill_date = models.DateField()
    due_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    penalty = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Bill {self.bill_id} for User {self.user.username}"
    
    class Meta:
        db_table = 'water_billing_system_billing'

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    bill = models.ForeignKey('Billing', on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    trans_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('card', 'Card'), ('online', 'Online')]) # Add more options

    def __str__(self):
        return f"Payment {self.payment_id} - {self.trans_id}"
    
    class Meta:
        db_table = 'water_billing_system_payment'

class MeterService(models.Model):
    service_id = models.AutoField(primary_key=True)
    meter = models.ForeignKey('Meter', on_delete=models.CASCADE, related_name='services')
    service_date = models.DateField()
    service_type = models.CharField(max_length=20, choices=[('installation', 'Installation'), ('repair', 'Repair'), ('maintenance', 'Maintenance')])
    service_details = models.TextField()
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service_type} on {self.service_date} - Cost: {self.service_cost}"
    
    class Meta:
        db_table = 'water_billing_system_meter_service'