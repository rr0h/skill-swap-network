from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    """Skill categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-folder', help_text="FontAwesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def get_skill_count(self):
        """Get number of skills in this category"""
        return self.skills.count()
    
    def get_absolute_url(self):
        return reverse('skills:category_detail', kwargs={'pk': self.pk})


class Skill(models.Model):
    """Skills that can be taught or learned"""
    
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Describe what you'll teach")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='skills')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skills_offered')
    
    # Skill details
    level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='intermediate')
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '2 hours', '1 week'")
    location_preference = models.CharField(
        max_length=20,
        choices=[
            ('online', 'Online'),
            ('in_person', 'In Person'),
            ('both', 'Both'),
        ],
        default='both'
    )
    
    # Metadata
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('skills:skill_detail', kwargs={'pk': self.pk})
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0
    
    def get_total_reviews(self):
        """Get total number of reviews"""
        return self.reviews.count()
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
