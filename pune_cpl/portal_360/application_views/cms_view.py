from ..models import *
from ..forms import ComplaintForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden

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
    
    if status_filter in ['Pending', 'Closed', 'Rejected']:
        complaints_list = complaints_list.filter(status=status_filter)

    paginator = Paginator(complaints_list, 10)
    page_obj = paginator.get_page(page_number)

    all_complaints = CMSComplaints.objects.all().count()
    solved_complaints = CMSComplaints.objects.filter(status="Closed").count()
    rejected_complaints = CMSComplaints.objects.filter(status="Rejected").count()
    pending_complaints = CMSComplaints.objects.filter(status="Pending").count()
    
    context = {
        'form': form,
        'all_complaints': all_complaints,
        'resolved_complaints': solved_complaints,
        'rejected_complaints': rejected_complaints,
        'pending_complaints': pending_complaints,
        'page_obj': page_obj,
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