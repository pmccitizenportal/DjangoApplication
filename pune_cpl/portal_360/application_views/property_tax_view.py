import json
import numpy as np
import pandas as pd
from ..models import *
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from collections import defaultdict
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models.functions import TruncMonth
from statsmodels.tsa.api import SimpleExpSmoothing
from babel.numbers import format_currency, format_decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Count, Max, F, Min

def get_biannual_forecast(property_ids):
    current_year = timezone.now().year
    df = pd.DataFrame(list(PropertyTaxAccountStatement.objects.filter(property_id__in=property_ids).values('payment_date', 'amount_paid')))
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    df.set_index('payment_date', inplace=True)
    df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
    df.dropna(inplace=True)
    
    df = df.resample('QS-JAN').sum()

    model = SimpleExpSmoothing(df['amount_paid'], initialization_method="estimated").fit()
    future_periods = 2
    forecast = model.forecast(future_periods)

    next_periods = [df.index[-1] + pd.DateOffset(months=6 * i) for i in range(1, future_periods + 1)]
    return list(zip(next_periods, [format_currency(value, 'INR', locale='en_IN') for value in forecast]))

def get_next_payment_period_tax(property_ids):
    today = now()
    current_year = today.year

    if today.month <= 6:
        next_period_start = datetime(current_year, 7, 1)
        next_period_end = datetime(current_year, 12, 31)
    else:
        next_period_start = datetime(current_year + 1, 1, 1)
        next_period_end = datetime(current_year + 1, 6, 30)

    forecast_data = get_biannual_forecast(property_ids)

    if forecast_data:
        if today.month <= 6:
            next_forecast = forecast_data[0][1] if forecast_data[0][0].month == 7 else forecast_data[1][1]
        else:
            next_forecast = forecast_data[1][1] if forecast_data[1][0].month == 1 else forecast_data[0][1]
    else:
        next_forecast = 0

    return {
        'from': next_period_start.strftime('%B %d, %Y'),
        'to': next_period_end.strftime('%B %d, %Y'),
        'amount': next_forecast
    }

def prepare_tax_billing_chart_data(property_ids):
    tax_records = PropertyTaxAccountStatement.objects.filter(
        property_id__in=property_ids,
    ).values('payment_date', 'amount_paid')

    df = pd.DataFrame(list(tax_records))
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    df.set_index('payment_date', inplace=True)
    df.sort_index(inplace=True)
    df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')

    monthly_data = df.resample('M').sum().reset_index()
    monthly_data['month'] = monthly_data['payment_date'].dt.strftime('%Y-%m')

    chart_data = {
        'labels': monthly_data['month'].tolist(),
        'data': monthly_data['amount_paid'].tolist()
    }
    return chart_data

@login_required
def property_tax_view(request):
    current_year = timezone.now().year
    user = request.user
    selected_property_id = request.GET.get('property_id')
    status_filter = request.GET.get('status_filter')
    
    if selected_property_id and selected_property_id != 'all':
        selected_property = PropertyTaxPropertyDetail.objects.filter(user=user, property_id=selected_property_id).first()
        account_statements = PropertyTaxAccountStatement.objects.filter(property_id=selected_property_id)
        
        total_tax_paid = account_statements.aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0
        
        total_billed_amount = account_statements.aggregate(total_billed=Sum('bill_amount'))['total_billed'] or 0
        
        outstanding_amount = total_billed_amount - total_tax_paid
        
        forecasted_amounts = get_biannual_forecast([selected_property_id])
        forecasted_next_period_amount = forecasted_amounts[0][1] if forecasted_amounts else "No Data"

        form_histories = PropertyTaxApplicationFormHistory.objects.filter(property_id=selected_property_id).order_by('-date_of_application')
        
        monthly_trends = account_statements.annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            total=Sum('property_tax')
        ).order_by('month')

        line_chart_data = {
            'labels': [trend['month'].strftime("%Y-%m") for trend in monthly_trends],
            'data': [float(trend['total']) for trend in monthly_trends],
        }

        line_chart_data_json = json.dumps(line_chart_data)
        
        full_payments = account_statements.filter(payment_status='Paid').count()
        partial_payments = account_statements.filter(payment_status='Partial Payment').count()

        pie_chart_data = {
            'labels': ['Full Payments', 'Partial Payments'],
            'values': [full_payments, partial_payments],
        }

        pie_chart_data_json = json.dumps(pie_chart_data)
        
        context = {
            'user': user,
            'selected_property': selected_property,
            'total_tax_paid': format_currency(total_tax_paid, 'INR', locale='en_IN'),
            'outstanding_amount': format_currency(outstanding_amount, 'INR', locale='en_IN'),
            'forecasted_next_period_amount': forecasted_next_period_amount,
            'form_histories': form_histories,
            'line_chart_data': line_chart_data_json,
            'pie_chart_data': pie_chart_data_json,
            'account_statements': account_statements,
        }
    else:
        selected_property = None
        
        properties = PropertyTaxPropertyDetail.objects.filter(user=user)
        property_ids = properties.values_list('property_id', flat=True)
        statements = PropertyTaxAccountStatement.objects.filter(property_id__in=property_ids, payment_date__year=current_year)
        paginator = Paginator(properties, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        total_properties = properties.count()
        average_market_value = format_currency(properties.aggregate(Avg('market_value'))['market_value__avg'], 'INR', locale='en_IN')
        total_carpet_area = format_decimal(properties.aggregate(Sum('carpet_area'))['carpet_area__sum'], locale='en_IN') + " sq ft"
        properties_rented = properties.filter(is_rental=True).count()
        average_construction_year = int(properties.aggregate(Avg('construction_year'))['construction_year__avg'])
        total_parking_spaces = properties.aggregate(Sum('no_of_parking_spaces'))['no_of_parking_spaces__sum']
        active_verifications = PropertyTaxActiveVerificationHistory.objects.filter(property_id__in=property_ids).count()
        total_tax_collected = format_currency(statements.aggregate(Sum('amount_paid'))['amount_paid__sum'], 'INR', locale='en_IN')
        average_age = str(int(properties.annotate(age=timezone.now().year - F('construction_year')).aggregate(Avg('age'))['age__avg'])) + " years"
        common_property_type = PropertyTaxPropertyDetail.objects.values('property_type').annotate(count=Count('property_type')).order_by('-count').first()
        highest_base_value = format_currency(properties.aggregate(Max('base_value'))['base_value__max'], 'INR', locale='en_IN')
        partial_payments = statements.filter(payment_status='partial').count()
        next_due_date = statements.filter(due_date__gte=timezone.now()).aggregate(Min('due_date'))['due_date__min']
        total_amount_collected = format_currency(statements.aggregate(Sum('amount_paid'))['amount_paid__sum'], 'INR', locale='en_IN')
        
        remaining_duration = f"{(next_due_date - timezone.now().date()).days} days" if next_due_date else 'N/A'
        
        tax_pie_chart_data = PropertyTaxAccountStatement.objects.filter(property_id__in=properties.values('property_id')) \
            .values('property_id') \
            .annotate(total_tax=Sum('property_tax')) \
            .order_by('-total_tax')
        
        tax_statements = PropertyTaxAccountStatement.objects.filter(property_id__in=properties.values('property_id'))
        monthly_data = tax_statements.annotate(month=TruncMonth('payment_date')).values('month', 'property_id').annotate(total=Sum('property_tax')).order_by('month')

        results = defaultdict(lambda: defaultdict(lambda: Decimal(0)))
        for entry in monthly_data:
            month = entry['month'].strftime('%Y-%m')
            results[month][entry['property_id']] += entry['total']

        for month in results:
            for prop_id in results[month]:
                results[month][prop_id] = str(results[month][prop_id])  #type: ignore

        plot_data = {
            'x': sorted(results),  # Sorted months
            'traces': defaultdict(list)
        }

        for month in sorted(results):
            for prop_id, value in results[month].items():
                plot_data['traces'][prop_id].append(value)
        
        form_histories = PropertyTaxApplicationFormHistory.objects.filter(property_id__in=properties.values('property_id')).order_by('property_id')
        if status_filter:
            form_histories = form_histories.filter(status=status_filter)
        
        form_history_paginator = Paginator(form_histories, 10)
        page_number = request.GET.get('form-page')
        form_page_obj = form_history_paginator.get_page(page_number)
        
        month_forecast_pairs = get_biannual_forecast(property_ids)
        next_payment_period = get_next_payment_period_tax(property_ids)
        
        context = {
            'user': user,
            'selected_property': selected_property,
            'page_obj': page_obj,
            'total_properties': total_properties,
            'average_market_value': average_market_value,
            'total_carpet_area': total_carpet_area,
            'properties_rented': properties_rented,
            'average_construction_year': average_construction_year,
            'total_parking_spaces': total_parking_spaces,
            'active_verifications': active_verifications,
            'total_tax_collected': total_tax_collected,
            'average_age': average_age,
            'common_property_type': common_property_type,
            'highest_base_value': highest_base_value,
            'total_amount_collected': total_amount_collected,
            'partial_payments': partial_payments,
            'next_due_date': next_due_date,
            'remaining_duration': remaining_duration,
            'tax_distribution': list(tax_pie_chart_data),
            'stacked_bar_data': json.dumps(plot_data),
            'form_histories': form_page_obj,
            'status_filter': status_filter,
            'month_forecast_pairs': month_forecast_pairs,
            'next_payment_period': next_payment_period,
            'billing_chart_data': prepare_tax_billing_chart_data(property_ids),
        }
    
    return render(request, 'property_tax.html', context)