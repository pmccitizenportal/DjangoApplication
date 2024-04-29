from django.db import models

class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True)
    ward_name = models.TextField()
    
    def __str__(self):
        return f"Ward {self.ward_id} {self.ward_name}"

    class Meta:
        db_table = 'ward_master'

class Peth(models.Model):
    peth_id = models.AutoField(primary_key=True)
    peth_name = models.TextField()
    ward_id = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='wards')

    def __str__(self):
        return f"Peth {self.peth_name} - {self.ward_id}"
    
    class Meta:
        db_table = 'peth_master'
        

class GIS(models.Model):
    gis_id = models.CharField(max_length=50, primary_key=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"GIS {self.gis_id} - {self.latitude} {self.longitude}"

    class Meta:
        db_table = 'gis_master'

class Pincode(models.Model):
    pincode_id = models.AutoField(primary_key=True)
    pincode = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    peth = models.TextField()
    ward = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    def __str__(self):
        return self.pincode
    
    class Meta:
        db_table = 'pincode_master'

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name

    class Meta:
        db_table = 'department_master'