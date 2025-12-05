from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    
    bio = models.TextField(max_length=500, blank=True, help_text="Tell others about yourself")
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        default='profile_images/default.jpg',
        help_text="Upload your profile picture"
    )
    location = models.CharField(max_length=100, blank=True, help_text="Your city or region")
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Profile completion tracking
    profile_completed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize profile image
        if self.profile_image:
            try:
                img = Image.open(self.profile_image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_image.path)
            except:
                pass
    
    def get_profile_completion(self):
        """Calculate profile completion percentage"""
        fields = [
            self.bio,
            self.location,
            self.phone,
            self.profile_image.name != 'profile_images/default.jpg',
        ]
        completed = sum(1 for field in fields if field)
        total = len(fields)
        return int((completed / total) * 100)
    
    def get_skills_offered(self):
        """Get skills this user can teach"""
        return self.skills_offered.all()
    
    def get_skills_wanted(self):
        """Get skills this user wants to learn"""
        return self.skills_wanted.all()
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.received_reviews.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0
    
    def get_total_reviews(self):
        """Get total number of reviews received"""
        return self.received_reviews.count()


class UserSkill(models.Model):
    """Skills that users offer or want to learn"""
    
    SKILL_TYPE_CHOICES = [
        ('offer', 'Can Teach'),
        ('want', 'Want to Learn'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill_name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPE_CHOICES)
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'skill_name', 'skill_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill_name} ({self.get_skill_type_display()})"
