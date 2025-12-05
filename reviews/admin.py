from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review admin"""
    list_display = ['reviewer', 'reviewed_user', 'skill', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__username', 'reviewed_user__username', 'skill__title', 'comment']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('reviewer', 'reviewed_user', 'skill', 'request')
        }),
        ('Ratings', {
            'fields': ('rating', 'communication_rating', 'knowledge_rating', 'patience_rating')
        }),
        ('Comment', {
            'fields': ('comment',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
