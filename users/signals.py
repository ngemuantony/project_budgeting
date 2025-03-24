from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.signals import email_confirmed
from .models import User, StaffUserProfile, EndUserProfile

User = get_user_model()

@receiver(email_confirmed)
def email_confirmed_handler(sender, request, email_address, **kwargs):
    """
    Handle email confirmation from django-allauth.
    Update the user's email_verified status.
    """
    user = email_address.user
    user.email_verified = True
    user.save()

@receiver(pre_save, sender=User)
def clean_user_email(sender, instance, **kwargs):
    """Ensure email is always stored in lowercase."""
    if instance.email:
        instance.email = instance.email.lower()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update user profile.
    This signal ensures that every user has associated profile data.
    """
    if created:
        # Set default values for new users
        instance.email_verified = False
        instance.save()
    print(f"Signal triggered for {instance.email}, created={created}, type={instance.type}")
    if created or (not created and instance.type != User.objects.get(pk=instance.pk).type):
        if instance.type == User.Types.STAFF:
            StaffUserProfile.objects.get_or_create(user=instance)
            EndUserProfile.objects.filter(user=instance).delete()
        elif instance.type == User.Types.ENDUSER:
            EndUserProfile.objects.get_or_create(user=instance)
            StaffUserProfile.objects.filter(user=instance).delete()
    print(f"Post-signal: Staff profiles={StaffUserProfile.objects.filter(user=instance).count()}, EndUser profiles={EndUserProfile.objects.filter(user=instance).count()}")