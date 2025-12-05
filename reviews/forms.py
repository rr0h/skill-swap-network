from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for creating reviews"""
    
    class Meta:
        model = Review
        fields = ['rating', 'communication_rating', 'knowledge_rating', 'patience_rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'communication_rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'knowledge_rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'patience_rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 5,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Share your experience with this skill exchange...'
            }),
        }
