import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

citizen_id_validator = RegexValidator(
    regex=r'^CZN\d{5}$',
    message=_("Citizen ID must be in the format 'CZN00001' where digits follow 'CZN'.")
)

class CustomPasswordValidator:
    def validate(self, password, user=None):
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#!%*?&])[A-Za-z\d@$#!%*?&]{8,}$"
        if not re.match(password_regex, password):
            raise ValidationError(
                ("Password must be at least 8 characters long, include uppercase and lowercase letters, "
                "a number, and a special character."),
                code='invalid_password'
            )

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long, include uppercase and lowercase letters, "
            "a number, and a special character."
        )
        
def validate_unique_mobile_number(value):
    if User.objects.filter(mobile_number=value).exists():
        raise ValidationError("This mobile number is already in use.")

def validate_unique_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("This email is already in use.")

def validate_unique_aadhar(value):
    if User.objects.filter(aadhar_card_id=value).exists():
        raise ValidationError("This Aadhar card number is already registered.")

def validate_unique_pan(value):
    if User.objects.filter(pan_card_id=value).exists():
        raise ValidationError("This PAN card number is already registered.")

def validate_unique_ration(value):
    if User.objects.filter(ration_card_id=value).exists():
        raise ValidationError("This Ration card number is already registered.")