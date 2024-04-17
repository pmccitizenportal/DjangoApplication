from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number', 'aadhar_card_id', 'pan_card_id', 'ration_card_id', 'gender', 'dob', 'place_of_birth', 'nationality', 'address', 'geographical_details', 'marital_status', 'spouse_name', 'children_details', 'employment_type', 'occupation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'aadhar_card_id', 'pan_card_id', 'ration_card_id')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
