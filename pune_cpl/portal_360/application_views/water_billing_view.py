import numpy as np
from ..models import *
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils.timezone import timedelta
from django.contrib.auth.decorators import login_required

def predict_next_months(billing_amounts, num_months=6):
    x = np.arange(len(billing_amounts))
    fit = np.polyfit(x, billing_amounts, 1)
    fit_fn = np.poly1d(fit)
    
    x_future = np.arange(len(billing_amounts), len(billing_amounts) + num_months)
    future_forecasts = fit_fn(x_future).clip(min=0)
    
    return future_forecasts

@login_required
def water_billing_system_view(request):
    user = request.user
    selected_meter_id = request.GET.get('meter_id')
    active_tab = request.GET.get('active_tab', 'account-statement')  # Default to 'account-statement'
    
    if selected_meter_id and selected_meter_id != 'all':
        selected_meter = WaterBillingMeter.objects.filter(user=user, meter_id=selected_meter_id).first()
        readings = WaterBillingReading.objects.filter(meter=selected_meter).order_by('-reading_date')[:5]
        bills = WaterBillingBilling.objects.filter(user=user).filter(meter=selected_meter).order_by('-bill_date')
        payments_context = []
        months = []
        billing_amount = []
        bill_payment_data = []
        for bill in bills:
            payments = WaterBillingPayment.objects.filter(bill=bill).order_by('payment_date')
            payment_details = {
                'bill_id': bill.bill_id,
                'bill_date': bill.bill_date,
                'due_date': bill.due_date,
                'bill_amount': bill.bill_amount,
                'penalty': bill.penalty,
                'month': bill.month,
                'year': bill.year,
                'from_date': bill.from_date,
                'to_date': bill.to_date,
                'payments': [],
            }
            
            months.append(bill.month)
            billing_amount.append(float(bill.bill_amount))

            for payment in payments:
                payment_info = {
                    'payment_id': payment.payment_id,
                    'payment_status': payment.payment_status,
                    'payment_date': payment.payment_date,
                    'trans_id': payment.trans_id,
                    'amount': payment.amount,
                    'method': payment.payment_method,
                    'remarks': payment.remarks
                }
                payments_context.append(payment)
                payment_details['payments'].append(payment_info)
            
            bill_payment_data.append(payment_details)
        
        months.reverse()
        billing_amount.reverse()
        forecasts = []
        month_forecast_pairs = []
        next_payment_period = []
        
        if months != []:
            last_billing_month = datetime.strptime(months[-1], "%B")

            forecasts = predict_next_months(billing_amount)
            future_months = [last_billing_month + timedelta(days=31 * i) for i in range(1, 7)]
            future_months = [date.strftime("%B") for date in future_months]

            month_forecast_pairs = list(zip(future_months, forecasts))
            next_payment_period = { 
                'from': f"{month_forecast_pairs[0][0]}-01st {datetime.now().year}",
                'to': f"{month_forecast_pairs[0][0]}-30th {datetime.now().year}",
                'amount': month_forecast_pairs[0][1]
            }
            
        ongoing_services = WaterBillingMeterService.objects.filter(meter=selected_meter, status='ongoing').order_by('-service_date')
        completed_services = WaterBillingMeterService.objects.filter(meter=selected_meter, status='completed').order_by('-service_date')
    else:
        selected_meter = None
        ongoing_services = WaterBillingMeterService.objects.filter(meter__user=user, status='ongoing').order_by('-service_date')
        completed_services = WaterBillingMeterService.objects.filter(meter__user=user, status='completed').order_by('-service_date')
        readings = WaterBillingReading.objects.all().order_by('-reading_date')[:5]
        bills = WaterBillingBilling.objects.filter(user=user).order_by('-bill_date')
        payments_context = []
        months = []
        billing_amount = []
        bill_payment_data = []
        for bill in bills:
            payments = WaterBillingPayment.objects.filter(bill=bill).order_by('payment_date')
            payment_details = {
                'bill_id': bill.bill_id,
                'bill_date': bill.bill_date,
                'due_date': bill.due_date,
                'bill_amount': bill.bill_amount,
                'penalty': bill.penalty,
                'month': bill.month,
                'year': bill.year,
                'from_date': bill.from_date,
                'to_date': bill.to_date,
                'payments': [],
            }
            
            months.append(bill.month)
            billing_amount.append(float(bill.bill_amount))

            for payment in payments:
                payment_info = {
                    'payment_id': payment.payment_id,
                    'payment_status': payment.payment_status,
                    'payment_date': payment.payment_date,
                    'trans_id': payment.trans_id,
                    'amount': payment.amount,
                    'method': payment.payment_method,
                    'remarks': payment.remarks
                }
                payments_context.append(payment)
                payment_details['payments'].append(payment_info)
            
            bill_payment_data.append(payment_details)
        
        months.reverse()
        billing_amount.reverse()
        forecasts = []
        month_forecast_pairs = []
        next_payment_period = []
        
        if months != []:
            last_billing_month = datetime.strptime(months[-1], "%B")

            forecasts = predict_next_months(billing_amount)
            future_months = [last_billing_month + timedelta(days=31 * i) for i in range(1, 7)]
            future_months = [date.strftime("%B") for date in future_months]

            month_forecast_pairs = list(zip(future_months, forecasts))
            next_payment_period = { 
                'from': f"{month_forecast_pairs[0][0]}-01st {datetime.now().year}",
                'to': f"{month_forecast_pairs[0][0]}-30th {datetime.now().year}",
                'amount': month_forecast_pairs[0][1]
            }
            
    
    context = {
        'user': user,
        'selected_meter': selected_meter,
        'readings': readings,
        'bill_payment_data': bill_payment_data,
        'payments': payments_context[:5],
        'months': months,
        'billing_amounts': billing_amount,
        'forecasted_values': forecasts,
        'month_forecast_pairs': month_forecast_pairs,
        'next_payment_period': next_payment_period,
        'ongoing_services': ongoing_services,
        'completed_services': completed_services,
        'active_tab': active_tab,
    }

    return render(request, 'water_billing_system.html', context)

@login_required
def get_bill_details_view(request, bill_id):
    if request:
        bill = WaterBillingBilling.objects.filter(pk=bill_id, user=request.user).first()
        if bill:
            data = {
                'bill_id': bill.bill_id,
                'bill_date': bill.bill_date.strftime('%Y-%m-%d'),
                'due_date': bill.due_date.strftime('%Y-%m-%d'),
                'bill_amount': str(bill.bill_amount),
                'penalty': str(bill.penalty),
                'month': bill.month,
                'year': bill.year,
                'from_date': bill.from_date.strftime('%Y-%m-%d') if bill.from_date else '',
                'to_date': bill.to_date.strftime('%Y-%m-%d') if bill.to_date else ''
            }
            return JsonResponse(data, safe=False)
        return JsonResponse({'error': 'Bill not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_transaction_details_view(request, transaction_id):
    try:
        transaction = WaterBillingPayment.objects.get(trans_id=transaction_id)
        data = {
            'transaction_id': transaction.trans_id,
            'payment_date': transaction.payment_date.strftime('%Y-%m-%d'),
            'amount': transaction.amount,
            'payment_method': transaction.payment_method,
            'status': transaction.payment_status,
            'remarks': transaction.remarks,
        }
        return JsonResponse(data)
    except WaterBillingPayment.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)