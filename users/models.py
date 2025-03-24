from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

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
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
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

    # Profile fields
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text=_("Upload your profile picture")
    )
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    bio = models.TextField(
        _("Bio"),
        max_length=500,
        blank=True,
        help_text=_("Tell us about yourself")
    )
    position = models.CharField(
        _("Position"),
        max_length=100,
        blank=True,
        help_text=_("Your role or position in the organization")
    )
    department = models.CharField(
        _("Department"),
        max_length=100,
        blank=True,
        help_text=_("Your department in the organization")
    )
    date_of_birth = models.DateField(
        _("Date of Birth"),
        null=True,
        blank=True,
        help_text=_("Your date of birth")
    )
    address = models.TextField(
        _("Address"),
        max_length=250,
        blank=True,
        help_text=_("Your address")
    )
    
    # Email verification status
    email_verified = models.BooleanField(
        _("Email Verified"),
        default=False,
        help_text=_("Designates whether this user has verified their email address.")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        """Get URL for user's detail view."""
        return reverse("users:detail", kwargs={"username": self.username})
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def get_initials(self):
        """Return user's initials for avatar placeholder."""
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[0].upper()
        elif self.email:
            return self.email[0].upper()
        return "U"

    def get_profile_picture_url(self):
        """Return the URL of the profile picture or None."""
        if self.profile_picture:
            return self.profile_picture.url
        return None

    @property
    def profile_picture_url(self):
        """Return the URL of the profile picture or a default image."""
        if self.profile_picture:
            return self.profile_picture.url
        return "/static/images/default-profile.png"


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