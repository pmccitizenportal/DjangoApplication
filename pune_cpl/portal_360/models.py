from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, validate_slug, MaxLengthValidator
from .common_data import NATIONALITIES
from django.contrib.auth.models import User
from django.conf import settings
from .application_models.water_billing_system_model import *
from django.core.exceptions import ValidationError
from .application_models.property_tax_model import *
from .application_models.master_tables import *
from .application_models.complaint_management_system_model import *
from .application_models.participatory_budget_model import *
from django.core.validators import MinValueValidator, MaxValueValidator
import re

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

def pan_card_validator(value):
    if value != "None":
        regex = r'^[A-Z]{5}\d{4}[A-Z]$'
        if not re.match(regex, value):
            raise ValidationError("PAN card number must be in the format: 'ABCDE1234F'.")

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, help_text="Please enter your username", unique=True, default=None)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'mobile_number', 'government_id', 'dob', 'gender', 'nationality', 'pin_code', 'city', 'state']

    objects = CustomUserManager()
    
    department = models.TextField(blank=True, help_text="Please enter your department, if PMC employee.")
    mobile_number = models.CharField(max_length=15, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )], blank=True, help_text="Enter mobile number with country code")

    aadhar_card_id = models.CharField(max_length=12, validators=[RegexValidator(
        regex=r'^\d{12}$',
        message="Aadhar card number must be 12 digits."
    )], default=None, blank=True, unique=True, null=True)
    pan_card_id = models.CharField(max_length=10, 
        validators=[pan_card_validator], default=None, blank=True, unique=True, null=True)
    ration_card_id = models.CharField(max_length=12, validators=[validate_slug], default=None, blank=True, unique=True, null=True)

    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default=None)
    dob = models.DateField(help_text="Enter your date of birth.", default=None, null=True)
    place_of_birth = models.CharField(max_length=100, help_text="Enter your place of birth.", default=None, null=True)
    nationality = models.CharField(max_length=100, help_text="Enter your nationality.", choices=NATIONALITIES, default=None, null=True)
    address = models.TextField(help_text="Enter your address.", default=None, null=True)
    government_id = models.CharField(max_length=20, choices=[('aadhar', 'Aadhar Card'), ('pan', 'PAN Card'), ('ration', 'Ration Card')], default=None, null=True)
    marital_status = models.CharField(max_length=15, choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], default=None, null=True)
    spouse_name = models.CharField(max_length=100, blank=True, null=True, help_text="Enter spouse's name if applicable.", default=None,)
    children_details = models.JSONField(blank=True, null=True, help_text="Enter children's names and ages as JSON.", default=None)
    employment_type = models.CharField(max_length=50, help_text="Enter your employment type.", default=None, null=True)
    occupation = models.CharField(max_length=100, help_text="Enter your occupation.", default=None, null=True)
    number_of_family_members = models.IntegerField(default=0, null=True)
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(regex=r'^\d{6}$', message="Enter a valid 6-digit pin code.")], default=None, null=True)
    city = models.CharField(max_length=100, default=None, null=True)
    state = models.CharField(max_length=100, default=None, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    age = models.IntegerField(null=True, blank=True)
    education_level = models.CharField(max_length=100, null=True, blank=True)
    household_income = models.CharField(max_length=100, null=True, blank=True)  # Assuming income as ranges are specified as strings
    household_size = models.IntegerField(null=True, blank=True)
    language_spoken_at_home = models.CharField(max_length=100, null=True, blank=True)
    disability_status = models.CharField(max_length=100, null=True, blank=True)
    internet_access = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

class ApplicationUsage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    application_name = models.CharField(max_length=255)
    usage_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'application_name')