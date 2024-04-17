from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [ path('', views.home_redirect, name='home'),
                path('login/', views.login_view, name='login'),
                path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                path('verify_otp/', views.verify_otp_view, name='verify_otp'),
                path('register/', views.register_view, name='register'),
                path('reset-password/', views.reset_password_view, name='reset_password'),
                path('reset-password/success/', views.reset_password_view, name='reset_password_success'),
                path('home/', views.home_view, name='home'),
                path('update-usage/', views.update_application_usage, name='update_usage'),
                path('water-billing-system/', views.water_billing_system_view, name='water_billing_system'),]