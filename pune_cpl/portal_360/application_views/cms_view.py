from ..models import *
from ..forms import ComplaintForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.db.models import Count, Avg, ExpressionWrapper, F, DurationField
from django.db.models.functions import TruncMonth

@login_required
def cms_view(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = CMSComplaints(
                user=request.user,
                registration_date=now(),
                status='Pending',
                complaint_type_id=form.cleaned_data['complaint_type'],
                complaint_sub_type_id=form.cleaned_data['complaint_sub_type'],
                subject=form.cleaned_data['subject'],
                description=form.cleaned_data['description'],
                attachments=form.cleaned_data.get('attachments'),
                address=form.cleaned_data.get('address'),
                pincode=form.cleaned_data.get('pincode'),
                peth=form.cleaned_data.get('peth'),
                ward=form.cleaned_data.get('ward'),
                # department=form.cleaned_data.get('department'),
            )
            complaint.save()
            return redirect('cms')
    else:
        form = ComplaintForm()
    
    status_filter = request.GET.get('status', 'All')
    page_number = request.GET.get('page', 1)
    complaints_list = CMSComplaints.objects.filter(user=request.user)
    complaints_list_all = CMSComplaints.objects.all()
    pending_complaints_list_user = CMSComplaints.objects.filter(user=request.user, status="Pending")
    
    if status_filter in ['Pending', 'Closed', 'Rejected']:
        complaints_list = complaints_list.filter(status=status_filter)
        complaints_list_all = complaints_list_all.filter(status=status_filter)
    else:
        complaints_list = CMSComplaints.objects.filter(user=request.user)
        complaints_list_all = CMSComplaints.objects.all()

    paginator = Paginator(complaints_list, 10)
    page_obj = paginator.get_page(page_number)
    
    paginator_all = Paginator(complaints_list_all, 10)
    page_obj_all = paginator_all.get_page(page_number)

    all_complaints = CMSComplaints.objects.all().count()
    solved_complaints = CMSComplaints.objects.filter(status="Closed").count()
    rejected_complaints = CMSComplaints.objects.filter(status="Rejected").count()
    pending_complaints = CMSComplaints.objects.filter(status="Pending").count()
    top_complaint_types = CMSComplaints.objects.values('complaint_type_id__complaint_type').annotate(count=Count('complaint_type_id__complaint_type')).order_by('-count')[:5]

    average_resolution_time = CMSComplaints.objects.filter(status='Closed').annotate(resolution_time=ExpressionWrapper(F('completion_date') - F('registration_date'), output_field=DurationField())).aggregate(average=Avg('resolution_time'))

    monthly_complaints = CMSComplaints.objects.annotate(month=TruncMonth('registration_date')).values('month').annotate(count=Count('complaint_id')).order_by('month')

    all_complaints_user = CMSComplaints.objects.filter(user=request.user).count()
    solved_complaints_user = CMSComplaints.objects.filter(status="Closed", user=request.user).count()
    rejected_complaints_user = CMSComplaints.objects.filter(status="Rejected", user=request.user).count()
    pending_complaints_user = CMSComplaints.objects.filter(status="Pending", user=request.user).count()
    top_complaint_types_user = CMSComplaints.objects.filter(user=request.user).values('complaint_type_id__complaint_type').annotate(count=Count('complaint_type_id__complaint_type')).order_by('-count')[:5]

    average_resolution_time_user = CMSComplaints.objects.filter(status='Closed', user=request.user).annotate(resolution_time=ExpressionWrapper(F('completion_date') - F('registration_date'), output_field=DurationField())).aggregate(average=Avg('resolution_time'))

    monthly_complaints_user = CMSComplaints.objects.filter(user=request.user).annotate(month=TruncMonth('registration_date')).values('month').annotate(count=Count('complaint_id')).order_by('month')
    
    statuses = ['Closed', 'Pending', 'Rejected']
    counts = [solved_complaints, pending_complaints, rejected_complaints]
    
    statuses_user = ['Closed', 'Pending', 'Rejected']
    counts_user = [solved_complaints_user, pending_complaints_user, rejected_complaints_user]
    
    complaint_types = CMSComplaintType.objects.annotate(total=Count('cmscomplaints')).order_by('complaint_type')
    data = {
        'types': [],
        'subtypes': {subtype.complaint_sub_type: [] for subtype in CMSComplaintSubType.objects.all()},
        'counts': []
    }

    for ctype in complaint_types:
        data['types'].append(ctype.complaint_type)
        for subtype, subtype_counts in data['subtypes'].items():
            count = CMSComplaints.objects.filter(complaint_type_id=ctype, complaint_sub_type_id__complaint_sub_type=subtype).count()
            subtype_counts.append(count)
    
    complaint_types = CMSComplaintType.objects.annotate(total=Count('cmscomplaints')).order_by('complaint_type')
    data_user = {
        'types': [],
        'subtypes': {subtype.complaint_sub_type: [] for subtype in CMSComplaintSubType.objects.all()},
        'counts': []
    }

    for ctype in complaint_types:
        data_user['types'].append(ctype.complaint_type)
        for subtype, subtype_counts in data_user['subtypes'].items():
            count = CMSComplaints.objects.filter(user=request.user, complaint_type_id=ctype, complaint_sub_type_id__complaint_sub_type=subtype).count()
            subtype_counts.append(count)
    
    context = {
        'form': form,
        'all_complaints': all_complaints,
        'resolved_complaints': solved_complaints,
        'rejected_complaints': rejected_complaints,
        'pending_complaints': pending_complaints,
        'top_complaint_types': top_complaint_types,
        'average_resolution_time': average_resolution_time,
        'monthly_complaints': monthly_complaints,
        'all_complaints_user': all_complaints_user,
        'resolved_complaints_user': solved_complaints_user,
        'rejected_complaints_user': rejected_complaints_user,
        'pending_complaints_user': pending_complaints_user,
        'top_complaint_types_user': top_complaint_types_user,
        'average_resolution_time_user': average_resolution_time_user,
        'monthly_complaints_user': monthly_complaints_user,
        'page_obj': page_obj,
        'page_obj_all': page_obj_all,
        'statuses': statuses,
        'counts': counts,
        'statuses_user': statuses_user,
        'counts_user': counts_user,
        'bar_chart_data': data,
        'bar_chart_data_user': data_user,
        'pending_complaints_list_user': pending_complaints_list_user,
    }
    return render(request, 'cms.html', context)

def get_cms_subtypes(request, type_id):
    subtypes = CMSComplaintSubType.objects.filter(complaint_type_id=type_id)
    return JsonResponse({"subtypes": list(subtypes.values('complaint_sub_type_id', 'complaint_sub_type'))})

def get_peths_for_ward(request, ward_id):
    peths = Peth.objects.filter(ward_id=ward_id).order_by('peth_name')
    peth_list = [{'peth_id': peth.peth_id, 'peth_name': peth.peth_name} for peth in peths]
    return JsonResponse({'peths': peth_list})

def submit_rating(request, complaint_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        complaint = CMSComplaints.objects.get(pk=complaint_id)
        if complaint.status == 'Closed' and not complaint.rating:
            complaint.rating = rating
            complaint.save()
        return redirect('cms')

def submit_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        complaint_id = request.POST.get('complaint_id')
        complaint = CMSComplaints.objects.get(pk=complaint_id)
        if request.user != complaint.user:
            return HttpResponseForbidden("You are not allowed to update this complaint.")
        if complaint.status == 'Closed':
            complaint.feedback = feedback
            complaint.save()
        return redirect('cms') 

def reopen_complaint(request, complaint_id):
    if request.method == 'POST':
        complaint = CMSComplaints.objects.get(pk=complaint_id)
        if complaint.status == 'Closed' and complaint.rating:
            complaint.status = 'Pending'
            complaint.reopen = True
            complaint.save()
        return redirect('cms')