from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User, EndUserProfile, StaffUserProfile


# Profile Inlines for User Admin
class StaffUserProfileInline(admin.StackedInline):
    model = StaffUserProfile
    can_delete = False
    verbose_name_plural = "Staff Profile"


class EndUserProfileInline(admin.StackedInline):
    model = EndUserProfile
    can_delete = False
    verbose_name_plural = "End User Profile"


User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """Admin interface for User model."""
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {
            "fields": (
                "username",
                "first_name",
                "last_name",
                "profile_picture",
                "phone_number",
                "bio",
                "position",
                "department",
                "date_of_birth",
                "address",
            )
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "username", "first_name", "last_name", "is_staff"]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering = ["email"]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]
    readonly_fields = ["last_login", "date_joined"]
    
    def get_fieldsets(self, request, obj=None):
        """Customize fieldsets based on whether this is an add or change form."""
        if not obj:
            # Only show necessary fields when adding a user
            return (
                (None, {
                    "classes": ("wide",),
                    "fields": ("email", "username", "password1", "password2"),
                }),
            )
        return super().get_fieldsets(request, obj)

    # Dynamically include the correct profile inline
    def get_inlines(self, request, obj=None):
        """Return the correct profile inline based on the user type."""
        if obj:
            if obj.type == User.Types.STAFF:
                return [StaffUserProfileInline]
            elif obj.type == User.Types.ENDUSER:
                return [EndUserProfileInline]
        return []

    # Ensure profile inline exists in the admin panel
    def get_queryset(self, request):
        """Ensure profiles are loaded efficiently."""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("staff_profile", "end_user_profile")


# Admin for Staff and End User Profiles
@admin.register(StaffUserProfile)
class StaffUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__email", "user__first_name", "user__last_name")


@admin.register(EndUserProfile)
class EndUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__email", "user__first_name", "user__last_name")