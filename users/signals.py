from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StaffUserProfile, EndUserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print(f"Signal triggered for {instance.email}, created={created}, type={instance.type}")
    if created or (not created and instance.type != User.objects.get(pk=instance.pk).type):
        if instance.type == User.Types.STAFF:
            StaffUserProfile.objects.get_or_create(user=instance)
            EndUserProfile.objects.filter(user=instance).delete()
        elif instance.type == User.Types.ENDUSER:
            EndUserProfile.objects.get_or_create(user=instance)
            StaffUserProfile.objects.filter(user=instance).delete()
    print(f"Post-signal: Staff profiles={StaffUserProfile.objects.filter(user=instance).count()}, EndUser profiles={EndUserProfile.objects.filter(user=instance).count()}")