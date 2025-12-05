from django import forms
from .models import SkillRequest, RequestMessage


class SkillRequestForm(forms.ModelForm):
    """Form for creating skill requests"""
    
    class Meta:
        model = SkillRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Tell the skill owner why you want to learn this skill...'
            }),
        }


class RequestMessageForm(forms.ModelForm):
    """Form for sending messages within a request"""
    
    class Meta:
        model = RequestMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Type your message...'
            }),
        }
