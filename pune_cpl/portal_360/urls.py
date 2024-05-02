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
                path('profile/edit/', views.edit_profile, name='profile'),
                path('update-usage/', views.update_application_usage, name='update_usage'),
                path('water-billing-system/', views.water_billing_system_view, name='water_billing_system'),
                path('get-bill-details/<int:bill_id>/', views.get_bill_details_view, name='get_bill_details'),
                path('get-transaction-details/<transaction_id>/', views.get_transaction_details_view, name='get_transaction_details'),
                path('property-tax/', views.property_tax_view, name='property_tax'),
                path('cms/', views.cms_view, name='cms'),
                path('get-cms-subtypes/<int:type_id>/', views.get_cms_subtypes, name='get_cms_subtypes'),
                path('get-peths-for-ward/<int:ward_id>/', views.get_peths_for_ward, name='get_peths_for_ward'),
                path('submit-rating/<int:complaint_id>/', views.submit_rating, name='submit_rating'),
                path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
                path('reopen-complaint/<int:complaint_id>/', views.reopen_complaint, name='reopen_complaint'),
                path('participatory_budget/', views.participatory_budget_view, name='participatory_budget'),
                path('get-project-details/', views.get_project_details, name='get-project-details')]