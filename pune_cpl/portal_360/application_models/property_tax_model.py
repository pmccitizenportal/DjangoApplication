from django.db import models
from django.conf import settings

class PropertyTaxPropertyDetail(models.Model):
    property_id = models.AutoField(primary_key=True)
    verification_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    peth_name = models.CharField(max_length=255)
    peth_id = models.IntegerField()
    ward_name = models.CharField(max_length=100)
    ward_id = models.IntegerField()
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10)
    pincode_id = models.IntegerField()
    year_of_occupancy = models.IntegerField()
    floor_number = models.IntegerField()
    construction_year = models.IntegerField()
    construction_type = models.CharField(max_length=100, choices=[('rcc', 'RCC'), ('patra_shed', 'Patra Shed'), ('load_bearing', 'Load bearing'), ('office', 'Office'), ('open_plot', 'Open Plot')])
    construction_type_id = models.IntegerField()
    property_type = models.CharField(max_length=100, choices=[('residential', 'Residential'), ('non-residential', 'Non-Residential'), ('open-plot', 'Open Plot')])
    property_type_id = models.IntegerField()
    property_subtype = models.CharField(max_length=100, choices=[('flat', 'Flat'), ('individual', 'Individual'), ('office', 'Office'), ('open_plot', 'Open Plot')])
    property_subtype_id = models.IntegerField()
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_rate_id = models.IntegerField()
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    carpet_area = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_parking_spaces = models.IntegerField()
    is_parking = models.BooleanField(default=False)
    is_rental = models.BooleanField(default=False)
    no_of_floors = models.IntegerField()
    gis_id = models.CharField(max_length=100, null=True, blank=True)
    base_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    market_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.property_id}"
    
    class Meta:
        db_table = 'property_tax_property_detail'

class PropertyTaxAccountStatement(models.Model):
    statement_id = models.AutoField(primary_key=True)
    property_id = models.IntegerField()
    due_date = models.DateField()
    payment_date = models.DateField()
    challan_number = models.CharField(max_length=100, null=True, blank=True)
    transaction_number = models.CharField(max_length=100, null=True, blank=True)
    base_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    floor_factor = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    age_factor = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    property_type_id = models.IntegerField()
    property_type = models.CharField(max_length=100)
    building_type_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    carpet_area = models.DecimalField(max_digits=10, decimal_places=2)
    capital_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_rate_id = models.IntegerField()
    property_tax = models.DecimalField(max_digits=15, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    penalty_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    pending_amount = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=50, null=True, blank=True, choices=[('paid', 'Paid'), ('partial', 'Partial'), ('unpaid', 'Unpaid')])
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('debit_card', 'Debit Card'), ('online_banking', 'Online Banking'), ('cheque', 'Cheque'), ('credit_card', 'Credit Card')])

    def __str__(self):
        return f"{self.statement_id} - {self.property_id}"
    
    class Meta:
        db_table = 'property_tax_account_statement'

class PropertyTaxApplicationForm(models.Model):
    form_id = models.AutoField(primary_key=True)
    form_number = models.CharField(max_length=100, unique=True)
    form_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.form_number} - {self.form_name}"

    class Meta:
        db_table = 'property_tax_application_form'

class PropertyTaxApplicationFormHistory(models.Model):
    application_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(PropertyTaxPropertyDetail, on_delete=models.CASCADE, related_name='property_tax_application_form')
    form_number = models.CharField(max_length=100)
    form_type = models.CharField(max_length=100)
    date_of_application = models.DateField()
    status = models.CharField(max_length=100)
    date_of_disposal = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    notices_docs_uploaded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.form_number} - {self.status}"
    
    class Meta:
        db_table = 'property_tax_application_form_history'

class PropertyTaxPropertyType(models.Model):
    property_type_id = models.AutoField(primary_key=True)
    property_type = models.CharField(max_length=100, choices=[('residential', 'Residential'), ('non-residential', 'Non-Residential'), ('open-plot', 'Open Plot')])

    def __str__(self):
        return self.property_type

    class Meta:
        db_table = 'property_tax_property_type'

class PropertyTaxTaxRate(models.Model):
    tax_id = models.AutoField(primary_key=True)
    property_type_id = models.ForeignKey(PropertyTaxPropertyType, on_delete=models.CASCADE, related_name="property_type_tax_rates")
    property_type = models.CharField(max_length=100, choices=[('residential', 'Residential'), ('non-residential', 'Non-Residential'), ('open-plot', 'Open Plot')])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.property_type_id} - {self.tax_rate}%"

    class Meta:
        db_table = 'property_tax_tax_rate'

class PropertyTaxActiveVerificationHistory(models.Model):
    verification_id = models.AutoField(primary_key=True)
    verification_date = models.DateTimeField()
    property_id = models.ForeignKey(PropertyTaxPropertyDetail, on_delete=models.CASCADE, related_name='property_tax_property_verfiication')
    verification_status = models.CharField(max_length=100)
    verifier_name = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)
    notices_docs_uploaded = models.BooleanField()

    def __str__(self):
        return f"{self.property_id} - {self.verification_date} - {self.verification_status}"

    class Meta:
        db_table = 'property_tax_active_vertification_history'

class PropertyTaxInactiveVerificationHistory(models.Model):
    verification_id = models.AutoField(primary_key=True)
    verification_date = models.DateTimeField()
    property_id = models.ForeignKey(PropertyTaxPropertyDetail, on_delete=models.CASCADE, related_name='property_tax_inactive_property_vertification')
    verification_status = models.CharField(max_length=100)
    verifier_name = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)
    notices_docs_uploaded = models.BooleanField()

    def __str__(self):
        return f"{self.property_id} - {self.verification_date} - {self.verification_status}"

    class Meta:
        db_table = 'property_tax_inactive_property_vertification'

class PropertyTaxPropertyAddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(PropertyTaxPropertyDetail, on_delete=models.CASCADE, related_name='property_tax_property_address')
    floor_number = models.IntegerField()
    flat_number = models.CharField(max_length=100)
    property_name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=100)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    peth_name = models.CharField(max_length=255)
    ward_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pincode = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.property_name}, {self.city}, {self.state}"
    
    class Meta:
        db_table = 'property_tax_property_address'

class PropertyTaxPropertySubtype(models.Model):
    property_subtype_id = models.AutoField(primary_key=True)
    property_subtype = models.CharField(max_length=100, choices=[('flat', 'Flat'), ('individual', 'Individual'), ('office', 'Office'), ('open_plot', 'Open Plot')])
    property_type_id = models.IntegerField()
    property_type = models.CharField(max_length=100, choices=[('residential', 'Residential'), ('non-residential', 'Non-Residential'), ('open-plot', 'Open Plot')])
    
    def __str__(self):
        return self.property_subtype
    
    class Meta:
        db_table = 'property_tax_property_subtype'
        
class PropertyTaxConstructionType(models.Model):
    construction_type_id = models.AutoField(primary_key=True)
    construction_type = models.CharField(max_length=100, choices=[('rcc', 'RCC'), ('patra_shed', 'Patra Shed'), ('load_bearing', 'Load bearing'), ('office', 'Office'), ('open_plot', 'Open Plot')])

    def __str__(self):
        return self.construction_type
    
    class Meta:
        db_table = 'property_tax_construction_type'