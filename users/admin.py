from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserSkill


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'location', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_image', 'location', 'phone', 'date_of_birth', 'profile_completed')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'bio', 'location')
        }),
    )


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    """User Skill admin"""
    list_display = ['user', 'skill_name', 'skill_type', 'proficiency_level', 'created_at']
    list_filter = ['skill_type', 'proficiency_level', 'created_at']
    search_fields = ['user__username', 'skill_name']
    date_hierarchy = 'created_at'
