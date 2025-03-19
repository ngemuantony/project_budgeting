from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.template.loader import render_to_string
from .models import Project, Budget, Expense, Category
from .forms import ProjectForm, BudgetFormSet, CategoryForm
from .utils.emails import send_project_status_email
import csv
from datetime import datetime
from decimal import Decimal

def landing_page(request):
    return render(request, "index.html")

def is_admin(user):
    return user.is_superuser

@login_required
def dashboard_landing_page(request):
    if request.user.is_superuser:
        return admin_dashboard(request)
    return user_dashboard(request)

@login_required
def user_dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    total_budget = sum(project.total_budget for project in projects)
    total_expenses = sum(project.total_expenses for project in projects)
    
    context = {
        'projects': projects,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'budget_remaining': total_budget - total_expenses,
    }
    return render(request, "dashboard.html", context)

@user_passes_test(is_admin)
def admin_dashboard(request):
    projects = Project.objects.all()
    pending_projects = projects.filter(status='pending')
    total_budget = sum(project.total_budget for project in projects)
    total_expenses = sum(project.total_expenses for project in projects)
    
    context = {
        'projects': projects,
        'pending_projects': pending_projects,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'budget_remaining': total_budget - total_expenses,
    }
    return render(request, "admin_dashboard.html", context)

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "projects/list.html", {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_superuser and project.owner != request.user:
        messages.error(request, "You don't have permission to view this project.")
        return redirect('project_list')
    
    expenses = project.expenses.all()
    budgets = project.budgets.all()
    
    context = {
        'project': project,
        'expenses': expenses,
        'budgets': budgets,
    }
    return render(request, "projects/detail.html", context)

@login_required
def project_create(request):
    form = ProjectForm()
    formset = BudgetFormSet()
    
    if request.method == "POST":
        form = ProjectForm(request.POST)
        formset = BudgetFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.status = 'pending'
            project.save()
            
            formset.instance = project
            formset.save()
            
            messages.success(request, f"Project '{project.name}' has been created successfully.")
            return redirect('app:project_detail', pk=project.pk)
    
    return render(request, "projects/forms/project_form.html", {
        'form': form,
        'formset': formset,
    })

@login_required
def add_expense(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    # Check if project is cancelled
    if project.status == 'cancelled':
        if request.headers.get('HX-Request'):
            return HttpResponse(
                'Cannot add expenses to a cancelled project.',
                status=403
            )
        messages.error(request, 'Cannot add expenses to a cancelled project.')
        return redirect('app:project_detail', pk=project_id)
    
    if request.method == "POST":
        # Handle form submission with HTMX
        amount = Decimal(request.POST.get('amount'))
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        date_incurred = request.POST.get('date_incurred')
        
        category = get_object_or_404(Category, pk=category_id)
        
        expense = Expense.objects.create(
            project=project,
            category=category,
            amount=amount,
            description=description,
            date_incurred=date_incurred,
            created_by=request.user
        )
        
        if request.headers.get('HX-Request'):
            response = HttpResponse(
                render_to_string(
                    "projects/partials/expense_row.html",
                    {'expense': expense}
                )
            )
            response['HX-Trigger'] = 'expenseAdded'
            return response
        return redirect('project_detail', pk=project_id)
    
    categories = Category.objects.all()
    return render(request, "projects/add_expense.html", {
        'project': project,
        'categories': categories
    })

@user_passes_test(is_admin)
def approve_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == "POST":
        project.status = 'approved'
        project.save()
        
        # Send email notification
        send_project_status_email(request, project)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Project "{project.name}" has been approved.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=400)

@login_required
def update_project_status(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == "POST":
        if not (request.user == project.owner or request.user.is_superuser):
            return JsonResponse({
                'status': 'error',
                'message': 'You do not have permission to update this project.'
            }, status=403)
        
        status = request.POST.get('status')
        if status not in dict(Project.STATUS_CHOICES):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid status.'
            }, status=400)
        
        project.status = status
        project.save()
        
        # Send email notification
        send_project_status_email(request, project)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Project status has been updated to {project.get_status_display()}.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=400)

@login_required
def cancel_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == "POST":
        if not (request.user == project.owner or request.user.is_superuser):
            return JsonResponse({
                'status': 'error',
                'message': 'You do not have permission to cancel this project.'
            }, status=403)
        
        project.status = 'cancelled'
        project.save()
        
        # Send email notification
        send_project_status_email(request, project)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Project "{project.name}" has been cancelled.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=400)

@user_passes_test(is_admin)
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == "POST":
        project_name = project.name
        project.delete()
        return JsonResponse({
            'status': 'success',
            'message': f'Project "{project_name}" has been deleted successfully.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=400)

@login_required
def export_project_report(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not request.user.is_superuser and project.owner != request.user:
        messages.error(request, "You don't have permission to export this project's report.")
        return redirect('project_list')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{project.name}_report_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Project Report', project.name])
    writer.writerow(['Start Date', project.start_date])
    writer.writerow(['End Date', project.end_date])
    writer.writerow(['Status', project.status])
    writer.writerow([])
    writer.writerow(['Category', 'Budgeted', 'Actual', 'Remaining'])
    
    for budget in project.budgets.all():
        actual = project.expenses.filter(category=budget.category).aggregate(Sum('amount'))['amount__sum'] or 0
        remaining = budget.amount - actual
        writer.writerow([
            budget.category.name,
            budget.amount,
            actual,
            remaining
        ])
    
    return response

@login_required
def profile_settings(request):
    """
    View for user profile settings
    """
    return render(request, 'account/profile_settings.html', {
        'user': request.user
    })

@login_required
def account_management(request):
    """
    View for account management page
    """
    return render(request, 'account/account_management.html', {
        'user': request.user
    })