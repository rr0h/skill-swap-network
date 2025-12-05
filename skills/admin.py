from django.contrib import admin
from .models import Category, Skill


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin"""
    list_display = ['name', 'get_skill_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'icon': ('name',)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Skill admin"""
    list_display = ['title', 'user', 'category', 'level', 'is_active', 'views_count', 'created_at']
    list_filter = ['is_active', 'level', 'location_preference', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'user')
        }),
        ('Skill Details', {
            'fields': ('level', 'duration', 'location_preference')
        }),
        ('Status & Metadata', {
            'fields': ('is_active', 'views_count', 'created_at', 'updated_at')
        }),
    )
