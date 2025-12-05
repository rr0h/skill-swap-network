from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def check_profile_completion(sender, instance, created, **kwargs):
    """Check if user profile is complete"""
    if not created:
        completion = instance.get_profile_completion()
        if completion == 100 and not instance.profile_completed:
            instance.profile_completed = True
            User.objects.filter(pk=instance.pk).update(profile_completed=True)
