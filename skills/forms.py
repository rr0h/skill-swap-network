from django import forms
from .models import Skill, Category


class SkillForm(forms.ModelForm):
    """Form for creating and editing skills"""
    
    class Meta:
        model = Skill
        fields = ['title', 'description', 'category', 'level', 'duration', 'location_preference']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'description':
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
                })


class SkillSearchForm(forms.Form):
    """Form for searching skills"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Search skills...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
        })
    )
    level = forms.ChoiceField(
        choices=[('', 'All Levels')] + Skill.SKILL_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
        })
    )
    location = forms.ChoiceField(
        choices=[
            ('', 'All Locations'),
            ('online', 'Online'),
            ('in_person', 'In Person'),
            ('both', 'Both'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
        })
    )
