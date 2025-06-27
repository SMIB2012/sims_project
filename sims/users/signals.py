from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, SupervisorProfile, ResidentProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update SupervisorProfile or ResidentProfile
    when a User instance is saved.
    """
    if instance.role == 'supervisor':
        # Check if it's a new user or role changed to supervisor
        if created or not hasattr(instance, 'supervisor_profile'):
            SupervisorProfile.objects.get_or_create(user=instance)
        # If role changed from pg, delete resident profile if it exists
        if hasattr(instance, 'resident_profile'):
            try:
                instance.resident_profile.delete()
            except ResidentProfile.DoesNotExist:
                pass # Profile already deleted or never existed
    elif instance.role == 'pg':
        # Check if it's a new user or role changed to pg
        if created or not hasattr(instance, 'resident_profile'):
            ResidentProfile.objects.get_or_create(user=instance)
        # If role changed from supervisor, delete supervisor profile if it exists
        if hasattr(instance, 'supervisor_profile'):
            try:
                instance.supervisor_profile.delete()
            except SupervisorProfile.DoesNotExist:
                pass # Profile already deleted or never existed
    else:
        # If role is admin or something else, ensure no profiles exist
        if hasattr(instance, 'supervisor_profile'):
            try:
                instance.supervisor_profile.delete()
            except SupervisorProfile.DoesNotExist:
                pass
        if hasattr(instance, 'resident_profile'):
            try:
                instance.resident_profile.delete()
            except ResidentProfile.DoesNotExist:
                pass
