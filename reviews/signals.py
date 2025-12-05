from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from notifications.models import Notification


@receiver(post_save, sender=Review)
def create_review_notification(sender, instance, created, **kwargs):
    """Create notification when a review is created"""
    if created:
        Notification.objects.create(
            user=instance.reviewed_user,
            notification_type='new_review',
            title='New Review Received',
            message=f'{instance.reviewer.username} left you a {instance.rating}-star review',
            link=f'/users/profile/{instance.reviewed_user.username}/'
        )
