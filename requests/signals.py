from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SkillRequest, RequestMessage
from notifications.models import Notification


@receiver(post_save, sender=SkillRequest)
def create_request_notification(sender, instance, created, **kwargs):
    """Create notification when request is created or updated"""
    if created:
        # New request notification
        Notification.objects.create(
            user=instance.receiver,
            notification_type='request_received',
            title='New Skill Request',
            message=f'{instance.sender.username} wants to learn {instance.skill.title}',
            link=f'/requests/{instance.pk}/'
        )
    else:
        # Status change notification
        if instance.status == 'accepted':
            Notification.objects.create(
                user=instance.sender,
                notification_type='request_accepted',
                title='Request Accepted',
                message=f'{instance.receiver.username} accepted your request for {instance.skill.title}',
                link=f'/requests/{instance.pk}/'
            )
        elif instance.status == 'rejected':
            Notification.objects.create(
                user=instance.sender,
                notification_type='request_rejected',
                title='Request Rejected',
                message=f'{instance.receiver.username} rejected your request for {instance.skill.title}',
                link=f'/requests/{instance.pk}/'
            )


@receiver(post_save, sender=RequestMessage)
def create_message_notification(sender, instance, created, **kwargs):
    """Create notification for new messages"""
    if created:
        # Determine recipient
        recipient = instance.request.receiver if instance.sender == instance.request.sender else instance.request.sender
        
        Notification.objects.create(
            user=recipient,
            notification_type='new_message',
            title='New Message',
            message=f'{instance.sender.username} sent you a message',
            link=f'/requests/{instance.request.pk}/'
        )
