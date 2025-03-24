from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, DetailView, ListView
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from .forms import (
    UserProfileForm,
    UserDeleteForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)

User = get_user_model()

class ProfileView(LoginRequiredMixin, DetailView):
    """View for displaying user profile."""
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user profile."""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Your profile has been updated successfully."))
        return super().form_valid(form)

@login_required
def profile_picture_upload(request):
    """AJAX view for handling profile picture uploads."""
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        return JsonResponse({
            'status': 'success',
            'message': _('Profile picture updated successfully.'),
            'url': user.profile_picture_url
        })
    return JsonResponse({
        'status': 'error',
        'message': _('No image file was provided.')
    }, status=400)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Custom view for changing password with improved styling."""
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Your password has been changed successfully."))
        update_session_auth_hash(self.request, form.user)
        return response

@login_required
def settings_view(request):
    """User settings view."""
    return render(request, 'users/profile.html', {
        'user': request.user,
    })

@login_required
def delete_account(request):
    """View for handling user account deletion."""
    if request.method == 'POST':
        form = UserDeleteForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['password']):
                user = request.user
                user.delete()
                messages.success(request, _("Your account has been deleted successfully."))
                return redirect('account_login')
            else:
                messages.error(request, _("The password you entered is incorrect."))
    else:
        form = UserDeleteForm()
    
    return render(request, 'users/delete-account.html', {'form': form})

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Admin view for listing all users."""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

@login_required
def toggle_user_status(request, user_id):
    """Admin view for toggling user active status."""
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user != request.user:  # Prevent self-deactivation
            user.is_active = not user.is_active
            user.save()
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(request, _(f"User {user.email} has been {status}."))
        else:
            messages.error(request, _("You cannot deactivate your own account."))
    
    return redirect('users:user_list')

@login_required
def toggle_staff_status(request, user_id):
    """Admin view for toggling user staff status."""
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user != request.user:  # Prevent self-demotion
            user.is_staff = not user.is_staff
            user.save()
            status = 'promoted to staff' if user.is_staff else 'demoted from staff'
            messages.success(request, _(f"User {user.email} has been {status}."))
        else:
            messages.error(request, _("You cannot change your own staff status."))
    
    return redirect('users:user_list')

@login_required
def profile_settings(request):
    """View for user profile settings."""
    return render(request, 'users/profile_edit.html', {
        'user': request.user,
    })

@login_required
def update_profile(request):
    """Update user profile information."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, _('Profile updated successfully'))
        return redirect('users:profile')
    return redirect('users:profile')

@login_required
def update_profile_picture(request):
    """Update user profile picture."""
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        messages.success(request, _('Profile picture updated successfully'))
    return redirect('users:profile_settings')
