from django.contrib import admin
from .models import SkillRequest, RequestMessage


@admin.register(SkillRequest)
class SkillRequestAdmin(admin.ModelAdmin):
    """Skill Request admin"""
    list_display = ['sender', 'receiver', 'skill', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'skill__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'accepted_at', 'completed_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('sender', 'receiver', 'skill', 'message')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'accepted_at', 'completed_at')
        }),
    )


@admin.register(RequestMessage)
class RequestMessageAdmin(admin.ModelAdmin):
    """Request Message admin"""
    list_display = ['request', 'sender', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'message']
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
