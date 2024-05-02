from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import Select, TextInput, PasswordInput, DateInput, Textarea, Textarea
from django.db.models import JSONField
from .common_data import NATIONALITIES, COMPLAINT_SUBTYPE_CHOICES, COMPLAINT_TYPE_CHOICES
from .validators import *
from .application_models.master_tables import *
from .models import *

User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(choices=[('citizen', 'Citizen'), ('officer', 'Officer')], widget=forms.RadioSelect)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your Username', 
        'id': 'username_input',
        'autofocus': True,
        'autocomplete': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password', 
        'id': 'password_input'
    }))

class OTPForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter the OTP', 'id': 'otp_input'}), max_length=4, help_text='Enter OTP (0000 to skip)')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Enter your Username', 'id': 'username_input', 'autofocus': True, 'autocomplete': 'username'}),
        max_length=150,
        required=True,
    )
    email = forms.EmailField(
        widget=TextInput(attrs={'placeholder': 'Enter your E-Mail', 'id': 'email_input'}),
        validators=[EmailValidator(), validate_unique_email],
        required=True,
    )
    government_id = forms.ChoiceField(
        choices=[('aadhar', 'Aadhar Card'), ('pan', 'PAN Card'), ('ration', 'Ration Card')],
        widget=Select(attrs={'id': 'government_id_input'}),
        required=True,
    )
    aadhar_card_id = forms.CharField(
        label='Aadhar Card ID',
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Aadhar Card ID', 'id': 'aadhar_card_id_input'}),
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."), validate_unique_mobile_number],
        required=False,
    )
    pan_card_id = forms.CharField(
        label='PAN Card ID',
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your PAN Card ID', 'id': 'pan_card_id_input'}),
        validators=[RegexValidator(regex=r'^[A-Z]{5}\d{4}[A-Z]$', message="Enter a valid PAN card number."), validate_unique_pan],
        required=False,
    )
    ration_card_id = forms.CharField(
        label='Ration Card ID',
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Ration Card ID', 'id': 'ration_card_id_input'}),
        validators=[RegexValidator(regex=r'^\d{12}$', message="Enter a valid 12-digit Ration card number."), validate_unique_ration],
        required=False,
    )
    password1 = forms.CharField(
        label='Password',
        widget=PasswordInput(attrs={'placeholder': 'Create a password', 'id': 'password1_input'}),
        required=True,
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=PasswordInput(attrs={'placeholder': 'Confirm your password', 'id': 'password2_input'}),
        required=True,
    )
    mobile_number = forms.CharField(
        label='Mobile Number',
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."), validate_unique_mobile_number],
        widget=TextInput(attrs={'placeholder': 'Enter your mobile number', 'id': 'mobile_number_input'}),
        required=True,
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your First Name', 'id': 'first_name_input'}),
        required=True,)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Last Name', 'id': 'last_name_input'}),
        required=True,)
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=Select(attrs={'id': 'gender_input'}),
        required=True,
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'dob_input', 'placeholder': 'YYYY-MM-DD'}),
        help_text="Format: YYYY-MM-DD",
        required=True,
    )
    place_of_birth = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Enter your place of birth', 'id': 'place_of_birth_input'}),
        max_length=100,
        required=False,
    )
    nationality = forms.ChoiceField(
        choices=NATIONALITIES,
        widget=forms.Select(attrs={'id': 'nationality_input'}),
        required=True,
    )
    address = forms.CharField(
        widget=Textarea(attrs={'placeholder': 'Enter your address', 'id': 'address_input'}),
        required=False,
    )
    marital_status = forms.ChoiceField(
        choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')],
        widget=Select(),
        required=False,
    )
    spouse_name = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Enter spouse\'s name', 'id': 'spouse_name_input'}),
        required=False
    )
    children_details = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Enter your children details, in format (Name, Age)', 'id': 'children_details_input'}),
        required=False
    )
    employment_type = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Enter your employment type', 'id': 'employment_type_input'}),
        required=False
    )
    occupation_type = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Enter your occupation', 'id': 'occupation_input'}),
        required=False
    )
    number_of_family_members = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Number of Family Members'}),
        required=False,)
    pin_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Pin Code'}),
        required=True,)
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}),
        required=True,)
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State'}),
        required=True,)
    latitude = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Latitude'}),
        required=False,)
    longitude = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Longitude'}),
        required=False,)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'mobile_number', 
            'first_name', 'last_name', 'dob', 'gender', 'nationality', 'address',
            'number_of_family_members', 'pin_code', 'city', 'state', 'latitude', 'longitude',
            'aadhar_card_id', 'pan_card_id', 'ration_card_id', 'marital_status', 
            'spouse_name', 'children_details', 'employment_type', 'occupation_type'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")
        return cleaned_data


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your Username',
        'autofocus': True,
        'autocomplete': 'username',
        'id': 'username_input',
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a password', 'id': 'new_password_input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'id': 'confirm_password_input'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        validate_password(new_password)
        validate_password(confirm_password)
        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("The two password fields must match.")
        return cleaned_data

    def save(self, username, new_password):
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

class CustomUserEditForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': True}),
        required=False
    )
    nationality = forms.ChoiceField(
        choices=NATIONALITIES,
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': True}),
        required=False
    )
    marital_status = forms.ChoiceField(
        choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')],
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': True}),
        required=False
    )
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'mobile_number', 
            'first_name', 'last_name', 'dob', 'gender', 'nationality', 'address',
            'number_of_family_members', 'pin_code', 'city', 'state', 'latitude', 'longitude',
            'aadhar_card_id', 'pan_card_id', 'ration_card_id', 'marital_status', 
            'spouse_name', 'children_details', 'employment_type',
        )
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'children_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        self.fields['pan_card_id'].required = False
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False
        self.fields['latitude'].validators = []
        self.fields['longitude'].validators = []

class ComplaintForm(forms.Form):
    complaint_type = forms.ModelChoiceField(
        queryset=CMSComplaintType.objects.all(),
        label="Category",
        empty_label="Select a Category",
        required=True
    )
    complaint_sub_type = forms.ModelChoiceField(
        queryset=CMSComplaintSubType.objects.all(),
        label="Sub-Category",
        empty_label="Select a Sub-Category after choosing a Category",
        required=True
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a brief summary of your complaint'}),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe your complaint in detail', 'rows': 5}),
        required=True
    )
    attachments = forms.FileField(
        widget=forms.FileInput(),
        required=False
    )
    address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the complaint address'}),
        required=True
    )
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.all(),
        label="Ward",
        required=True,
        empty_label="Select the Ward",
    )
    peth = forms.ModelChoiceField(
        queryset=Peth.objects.all(),
        label="Peth",
        required=True,
        empty_label="Select the Peth",
    )
    pincode = forms.ModelChoiceField(
        queryset=Pincode.objects.all(),
        label="Pincode",
        required=True,
        empty_label="Select the Pincode",
    )
    # department = forms.ModelChoiceField(
    #     queryset=Department.objects.all(),
    #     label="Department",
    #     required=True,
    #     empty_label="Select the department",
    # )

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            initial_type_id = kwargs['initial'].get('complaint_type')
            if initial_type_id:
                self.fields['complaint_sub_type'].queryset = CMSComplaintSubType.objects.filter(complaint_type_id=initial_type_id)
        elif 'data' in kwargs:
            data = kwargs['data']
            type_id = data.get('complaint_type')
            if type_id:
                self.fields['complaint_sub_type'].queryset = CMSComplaintSubType.objects.filter(complaint_type_id=type_id)

    def clean_complaint_sub_type(self):
        sub_type_id = self.cleaned_data.get('complaint_sub_type')
        type_id = self.cleaned_data.get('complaint_type')
        if sub_type_id and not CMSComplaintSubType.objects.filter(complaint_type_id=type_id, pk=sub_type_id.pk).exists():
            raise forms.ValidationError("Select a valid choice. That choice is not one of the available choices.")
        return sub_type_id

class PBProjectFilterForm(forms.Form):
    department_id = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'style': 'width: 100%'}),
        label="Department"
    )
    ward_id = forms.ModelMultipleChoiceField(
        queryset=Ward.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'style': 'width: 100%'}),
        label="Ward"
    )
    project_id = forms.ModelMultipleChoiceField(
        queryset=PBProjects.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'style': 'width: 100%'}),
        label="Project"
    )
    min_timestamp = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    max_timestamp = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
class PBProjectSuggestionForm(forms.ModelForm):
    class Meta:
        model = PBProjects
        fields = ['project_category', 'project_title', 'description', 'ward', 'cost_estimate', 'priority_level', 'requested_deadline', 'supporting_documents']
        widgets = {
            'project_category': forms.Select(attrs={'class': 'form-control'}),
            'ward': forms.Select(attrs={'class': 'form-control'}),
            'cost_estimate': forms.Select(attrs={'class': 'form-control'}),
            'priority_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'requested_deadline': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'supporting_documents': forms.FileInput(attrs={'class': 'form-control'}),
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'project_category': 'Project Category',
            'project_title': 'Project Title',
            'description': 'Description',
            'ward': 'Ward Name',
            'cost_estimate': 'Cost Estimate',
            'priority_level': 'Priority Level (1-5)',
            'requested_deadline': 'Requested Deadline',
            'supporting_documents': 'Attach Supporting Documents',
        }
        help_texts = {
            'project_title': 'Enter the title of the project.',
            'description': 'Provide a detailed description of the project.',
        }