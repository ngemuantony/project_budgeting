from django.urls import path
from .views import (
    landing_page, dashboard_landing_page, project_list, project_detail,
    add_expense, approve_project, export_project_report, admin_dashboard,
    project_create, profile_settings, account_management, update_project_status,
    cancel_project, delete_project
)

app_name = 'app'
urlpatterns = [
    path('', landing_page, name="landing_page"),
    path('dashboard/', dashboard_landing_page, name="dashboard_landing_page"),
    path('admin-dashboard/', admin_dashboard, name="admin_dashboard"),
    path('projects/', project_list, name="project_list"),
    path('projects/create/', project_create, name="project_create"),
    path('projects/<int:pk>/', project_detail, name="project_detail"),
    path('projects/<int:project_id>/add-expense/', add_expense, name="add_expense"),
    path('projects/<int:project_id>/approve/', approve_project, name="approve_project"),
    path('projects/<int:project_id>/export/', export_project_report, name="export_project_report"),
    path('projects/<int:project_id>/update-status/', update_project_status, name='update_project_status'),
    path('projects/<int:project_id>/cancel/', cancel_project, name='cancel_project'),
    path('projects/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('profile/settings/', profile_settings, name="profile_settings"),
    path('account/', account_management, name="account_management"),
]
