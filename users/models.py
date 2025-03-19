from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser, PermissionsMixin):
    class Types(models.TextChoices):
        STAFF = "STAFF", "Staff"
        ENDUSER = "ENDUSER", "End User"

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True
    )
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    gender = models.CharField(
        _("Gender"), max_length=30, choices=GENDER_CHOICES, blank=True, null=True
    )
    type = models.CharField(
        _("User Type"),
        max_length=50,
        choices=Types.choices,
        default=Types.STAFF,
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user has verified their email.")
    )
    is_custom_admin = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user has dashboard access to the site.")
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


# Type-Based Query Managers
class StaffManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STAFF)


class EndUserManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ENDUSER)


# Staff Profile Model
class StaffUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"


# End User Profile Model
class EndUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="end_user_profile")

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "End User Profile"
        verbose_name_plural = "End User Profiles"



# Staff Proxy Model
class Staff(User):
    objects = StaffManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STAFF
        return super().save(*args, **kwargs)

    @property
    def profile(self):
        try:
            return self.staff_profile
        except StaffUserProfile.DoesNotExist:
            return None  # Or handle as needed


# EndUser Proxy Model
class EndUser(User):
    objects = EndUserManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.ENDUSER
        return super().save(*args, **kwargs)

    @property
    def profile(self):
        try:
            return self.end_user_profile
        except EndUserProfile.DoesNotExist:
            return None  # Or handle as needed
    
    
# Optimized Signal for Creating & Updating Profiles
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     """Ensure only the correct profile exists when a user is created or updated."""
#     if created or instance.type != User.objects.get(pk=instance.pk).type:
#         if instance.type == User.Types.STAFF:
#             StaffUserProfile.objects.get_or_create(user=instance)
#             EndUserProfile.objects.filter(user=instance).delete()
#         elif instance.type == User.Types.ENDUSER:
#             EndUserProfile.objects.get_or_create(user=instance)
#             StaffUserProfile.objects.filter(user=instance).delete()
            

import users.signals