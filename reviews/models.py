from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from skills.models import Skill
from requests.models import SkillRequest


class Review(models.Model):
    """Reviews for completed skill exchanges"""
    
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    reviewed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='reviews')
    request = models.OneToOneField(
        SkillRequest,
        on_delete=models.CASCADE,
        related_name='review',
        null=True,
        blank=True
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 to 5 stars"
    )
    comment = models.TextField(help_text="Share your experience")
    
    # Additional rating categories
    communication_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    knowledge_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    patience_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['reviewer', 'request']
    
    def __str__(self):
        return f"{self.reviewer.username} -> {self.reviewed_user.username}: {self.rating}★"
    
    def get_average_detailed_rating(self):
        """Calculate average of detailed ratings"""
        return round((self.communication_rating + self.knowledge_rating + self.patience_rating) / 3, 1)
