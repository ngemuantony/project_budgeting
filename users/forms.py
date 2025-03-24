from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm, ResetPasswordForm

User = get_user_model()

class UserAdminChangeForm(admin_forms.UserChangeForm):
    """Form for User model admin interface."""
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = "__all__"

class UserAdminCreationForm(admin_forms.UserCreationForm):
    """Form for User model creation in the admin interface."""
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }

class UserSignupForm(SignupForm):
    """Form for user registration."""
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'profile_picture', 'phone_number',
            'bio', 'position', 'department', 'date_of_birth', 'address'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class CustomPasswordResetForm(PasswordResetForm):
    """Custom form for password reset with improved styling."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email address')
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    """Custom form for setting new password with improved styling."""
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter new password')
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm new password')
        })
    )

class UserDeleteForm(forms.Form):
    """Form for user account deletion confirmation."""
    confirm_deletion = forms.BooleanField(
        required=True,
        label=_("I understand that this action cannot be undone"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password to confirm')
        })
    )

class CustomResetPasswordForm(ResetPasswordForm):
    # Example: Add custom field to the form
    custom_field = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Custom Field'}))

    def clean_custom_field(self):
        # Add custom validation logic for the custom field
        custom_value = self.cleaned_data.get('custom_field')
        if custom_value and len(custom_value) < 5:
            raise forms.ValidationError("Custom field must be at least 5 characters.")
        return custom_value

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
