from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import ResetPasswordForm

from .models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
        


class CustomResetPasswordForm(ResetPasswordForm):
    # Example: Add custom field to the form
    custom_field = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Custom Field'}))

    def clean_custom_field(self):
        # Add custom validation logic for the custom field
        custom_value = self.cleaned_data.get('custom_field')
        if custom_value and len(custom_value) < 5:
            raise forms.ValidationError("Custom field must be at least 5 characters.")
        return custom_value
