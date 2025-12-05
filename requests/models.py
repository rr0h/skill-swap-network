from django.db import models
from django.conf import settings
from skills.models import Skill


class SkillRequest(models.Model):
    """Skill exchange requests"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_requests'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_requests'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='requests')
    
    message = models.TextField(help_text="Why do you want to learn this skill?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['sender', 'skill', 'status']
    
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.skill.title}"
    
    def can_accept(self):
        """Check if request can be accepted"""
        return self.status == 'pending'
    
    def can_reject(self):
        """Check if request can be rejected"""
        return self.status == 'pending'
    
    def can_complete(self):
        """Check if request can be completed"""
        return self.status == 'accepted'
    
    def can_cancel(self):
        """Check if request can be cancelled"""
        return self.status in ['pending', 'accepted']


class RequestMessage(models.Model):
    """Messages within a skill request"""
    
    request = models.ForeignKey(SkillRequest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"
