from typing import Any
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    """Custom account adapter for django-allauth."""

    def is_open_for_signup(self, request: HttpRequest) -> bool:
        """Check if registration is allowed."""
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=True):
        """Save the newly registered user."""
        user = super().save_user(request, user, form, commit=False)
        
        # Set additional fields from the form
        data = form.cleaned_data
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        
        if commit:
            user.save()
        return user

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Get the URL to redirect to after email confirmation."""
        url = super().get_email_confirmation_url(request, emailconfirmation)
        return url

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """Send the confirmation email."""
        super().send_confirmation_mail(request, emailconfirmation, signup)
        
        # Update email_verified status once email is confirmed
        if not signup:
            user = emailconfirmation.email_address.user
            user.email_verified = True
            user.save()
