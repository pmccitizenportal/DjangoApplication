from ..models import *
from django.utils import timezone
from django.shortcuts import render, redirect
from ..forms import PBProjectFilterForm, PBProjectSuggestionForm
from django.db.models import Sum, Count, Q
from babel.numbers import format_currency, format_decimal
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

def participatory_budget_view(request):
    if request.method == 'POST':
        project_suggestion_form = PBProjectSuggestionForm(request.POST, request.FILES)
        if project_suggestion_form.is_valid():
            new_project = project_suggestion_form.save(commit=False)
            new_project.user = request.user
            new_project.save()
            return redirect('participatory_budget')
    else:
        project_suggestion_form = PBProjectSuggestionForm()
    
    form = PBProjectFilterForm(request.GET or None)
    page_number = request.GET.get('page', 1)
    page_number_2 = request.GET.get('page2', 1)
    projects = PBProjects.objects.all()
    user_projects_list = PBProjects.objects.filter(user=request.user)
    paginator = Paginator(user_projects_list, 10)
    page_obj = paginator.get_page(page_number)
    approved_ongoing_project_list = PBProjects.objects.filter(
        Q(final_implementation_status='Approved') | Q(final_implementation_status='Ongoing')
    )
    paginator_all = Paginator(approved_ongoing_project_list, 10)
    page_obj_filtered = paginator_all.get_page(page_number_2)
    
    if form.is_valid():
        department_ids = form.cleaned_data.get('department_id')
        ward_ids = form.cleaned_data.get('ward_id')
        project_ids = form.cleaned_data.get('project_id')
        min_timestamp = form.cleaned_data.get('min_timestamp')
        max_timestamp = form.cleaned_data.get('max_timestamp')

        if department_ids:
            projects = projects.filter(department_id__in=department_ids)
        if ward_ids:
            projects = projects.filter(ward_id__in=ward_ids)
        if project_ids:
            projects = projects.filter(project_id__in=project_ids)
        if min_timestamp:
            projects = projects.filter(submission_timestamp__gte=min_timestamp)
        if max_timestamp:
            projects = projects.filter(submission_timestamp__lte=max_timestamp)

    total_projects = projects.count()
    approved_projects = projects.filter(final_implementation_status='Approved').count()
    ongoing_projects = projects.filter(final_implementation_status='Ongoing').count()
    completed_projects = projects.filter(final_implementation_status='Completed').count()
    rejected_projects = projects.filter(final_implementation_status='Rejected').count()
    total_budget = projects.aggregate(total_budget=Sum('allocated_budget'))['total_budget']
    total_votes = projects.aggregate(total_votes=Sum('total_votes_received'))['total_votes']
    user_projects = projects.filter(user=request.user).count()
    active_projects = projects.filter(final_implementation_status__in=['Approved', 'Ongoing']).count()

    projects = projects.select_related('department', 'project_category').all()

    data = {}
    for project in projects:
        dept_name = project.department.department_name
        category_name = project.project_category.project_category_name
        if dept_name not in data:
            data[dept_name] = {}
        if category_name not in data[dept_name]:
            data[dept_name][category_name] = 0
        data[dept_name][category_name] += 1

    stacked_bar_data = []
    for dept, categories in data.items():
        for category, count in categories.items():
            stacked_bar_data.append({
                'x': [count],
                'y': [dept],
                'type': 'bar',
                'name': category,
                'orientation': 'h'
            })
            
    voting_data = PBVoting.objects.select_related('project__department').values('project__department__department_name').annotate(total_votes=Sum('voting_id')).order_by()
    
    total_votes = sum(item['total_votes'] for item in voting_data)

    plotly_voting_data = [{
        'x': [item['project__department__department_name'] for item in voting_data],
        'y': [(item['total_votes'] / total_votes * 100) for item in voting_data],
        'type': 'bar',
        'name': 'Voting Percentage'
    }]

    budget_data = PBBudget.objects.values('department__department_name').annotate(total_budget=Sum('allocated_budget')).order_by()

    labels = [item['department__department_name'] for item in budget_data]
    values = [float(item['total_budget']) for item in budget_data]

    plotly_budget_data = [{
        'labels': labels,
        'values': values,
        'type': 'pie',
        'name': 'Department Budgets',
        'hoverinfo': 'label+percent',
        'textinfo': 'value'
    }]
    
    age_brackets = [(0, 18), (19, 30), (31, 45), (46, 60), (61, 150)]
    age_bracket_labels = ['0-18', '19-30', '31-45', '46-60', '61+']

    family_size_data = {size: [] for size in range(1, 6)}

    for bracket in age_brackets:
        for size in range(1, 6):
            count = CustomUser.objects.filter(
                age__gte=bracket[0], age__lte=bracket[1], household_size=size
            ).count()
            family_size_data[size].append(count)

    plotly_age_data = []
    for size, counts in family_size_data.items():
        plotly_age_data.append({
            'x': age_bracket_labels,
            'y': counts,
            'type': 'bar',
            'name': f'Family Size {size}'
        })
    
    satisfaction_counts = projects.values('citizen_rating').annotate(count=Count('citizen_rating')).order_by('citizen_rating')
    satisfaction_labels = [f'Rating {x["citizen_rating"]}' for x in satisfaction_counts]
    satisfaction_values = [x['count'] for x in satisfaction_counts]

    satisfaction_data = {
        'labels': satisfaction_labels,
        'values': satisfaction_values,
        'type': 'pie',
        'name': 'Citizen Satisfaction',
        'hoverinfo': 'label+percent',
        'textinfo': 'value'
    }
    
    context = {
        'form': form,
        'project_suggestion_form': project_suggestion_form,
        'projects': projects,
        'total_projects': total_projects,
        'approved_projects': approved_projects,
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
        'total_budget': total_budget if total_budget else 0,
        'total_votes': total_votes if total_votes else 0,
        'user_projects': user_projects,
        'active_projects': active_projects,
        'rejected_projects': rejected_projects,
        'stacked_bar_data': stacked_bar_data,
        'plotly_voting_data': plotly_voting_data,
        'plotly_budget_data': plotly_budget_data,
        'plotly_age_data': plotly_age_data,
        'page_obj': page_obj,
        'page_obj_filtered': page_obj_filtered,
        'satisfaction_data': satisfaction_data,
    }

    return render(request, 'participatory_budget.html', context)

def get_project_details(request):
    project_id = request.GET.get('project_id')
    if project_id:
        project = PBProjects.objects.get(project_id=project_id)
        context = {'project': project}
        if request.GET.get('format') == 'html':
            html = render_to_string('partials/project_details.html', context)
            return HttpResponse(html)
        return JsonResponse(model_to_dict(project))
    else:
        return JsonResponse({'error': 'Project ID not provided'}, status=400)