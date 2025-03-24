from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Profile views
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/picture/upload/", views.profile_picture_upload, name="profile_picture_upload"),
    path("profile/settings/", views.profile_settings, name="profile_settings"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("profile/update-picture/", views.update_profile_picture, name="update_profile_picture"),
    
    # Settings
    path("settings/", views.settings_view, name="settings"),
    
    # Password management
    path("password/change/", views.CustomPasswordChangeView.as_view(), name="password_change"),
    path("delete-account/", views.delete_account, name="delete_account"),
    
    # Admin user management
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:user_id>/toggle-status/", views.toggle_user_status, name="toggle_user_status"),
    path("users/<int:user_id>/toggle-staff/", views.toggle_staff_status, name="toggle_staff_status"),
]
