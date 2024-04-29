from .models import *
from django.contrib import messages
from django.http import JsonResponse
from .models import ApplicationUsage
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .application_views.property_tax_view import *
from .application_views.water_billing_view import *
from .application_views.cms_view import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, OTPForm, CustomUserCreationForm, ResetPasswordForm, CustomUserEditForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST, request=request)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            user = form.get_user()
            
            if user_type == 'officer' and not (user.is_staff and user.department):
                messages.error(request, "Unauthorized access for officer login.")
                return render(request, 'login.html', {'form': form})
            
            login(request, user)
            return redirect('verify_otp')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == '0000':
                return redirect('home')
            else:
                messages.error(request, "Invalid OTP")
                return render(request, 'login.html', {'otp_form': form})
    else:
        form = OTPForm()
    return render(request, 'login.html', {'otp_form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def home_redirect(request):
    return redirect('login')

def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = form.cleaned_data['new_password']
            form.save(username, password)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('login')
        else:
            return render(request, 'reset_password.html', {'form': form})
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})

@login_required
def home_view(request):
    user = request.user
    all_applications = ['Property Tax', 'Water Billing System', 'Participatory Budget', 'Complaint Management System', 'Legal Department', 'Shahari Garib Yojana', 'Local Body Tax', 'Slum Department Billing', 'Hawkers Management System', 'Building Permission', 'Geographic Information System', 'Chatbot']
    frequently_used = ApplicationUsage.objects.filter(user=user).order_by('-usage_count')[:3]

    return render(request, 'home.html', {
        'all_applications': all_applications,
        'frequently_used': frequently_used,
    })

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'profile.html', {'form': form})

@login_required
@require_POST
def update_application_usage(request):
    app_name = request.POST.get('application_name')
    user = request.user
    if not app_name:
        return JsonResponse({'error': 'Missing application name'}, status=400)

    app_usage, created = ApplicationUsage.objects.get_or_create(
        user=user,
        application_name=app_name,
        defaults={'usage_count': 1}
    )
    if not created:
        app_usage.usage_count += 1
        app_usage.save()

    return JsonResponse({'usage_count': app_usage.usage_count})