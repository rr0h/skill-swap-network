from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Skill, Category
from .forms import SkillForm, SkillSearchForm


def skill_list(request):
    """List all skills with search and filter"""
    skills = Skill.objects.filter(is_active=True).select_related('user', 'category')
    form = SkillSearchForm(request.GET)
    
    # Search and filter
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        level = form.cleaned_data.get('level')
        location = form.cleaned_data.get('location')
        
        if query:
            skills = skills.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(user__username__icontains=query)
            )
        
        if category:
            skills = skills.filter(category=category)
        
        if level:
            skills = skills.filter(level=level)
        
        if location:
            skills = skills.filter(location_preference=location)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'popular':
        skills = skills.order_by('-views_count')
    elif sort_by == 'rating':
        skills = skills.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        skills = skills.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(skills, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_skills': skills.count(),
    }
    
    return render(request, 'skills/skill_list.html', context)


def skill_detail(request, pk):
    """Skill detail view"""
    skill = get_object_or_404(Skill.objects.select_related('user', 'category'), pk=pk)
    skill.increment_views()
    
    # Get related skills
    related_skills = Skill.objects.filter(
        category=skill.category,
        is_active=True
    ).exclude(pk=skill.pk)[:4]
    
    context = {
        'skill': skill,
        'related_skills': related_skills,
        'can_request': request.user.is_authenticated and request.user != skill.user,
    }
    
    return render(request, 'skills/skill_detail.html', context)


@login_required
def skill_create(request):
    """Create a new skill"""
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill created successfully!')
            return redirect('skills:skill_detail', pk=skill.pk)
    else:
        form = SkillForm()
    
    return render(request, 'skills/skill_form.html', {'form': form, 'title': 'Create Skill'})


@login_required
def skill_update(request, pk):
    """Update a skill"""
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('skills:skill_detail', pk=skill.pk)
    else:
        form = SkillForm(instance=skill)
    
    return render(request, 'skills/skill_form.html', {'form': form, 'title': 'Edit Skill', 'skill': skill})


@login_required
def skill_delete(request, pk):
    """Delete a skill"""
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully!')
        return redirect('skills:skill_list')
    
    return render(request, 'skills/skill_confirm_delete.html', {'skill': skill})


def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'skills/category_list.html', context)


def category_detail(request, pk):
    """Category detail with skills"""
    category = get_object_or_404(Category, pk=pk)
    skills = Skill.objects.filter(category=category, is_active=True).select_related('user')
    
    # Pagination
    paginator = Paginator(skills, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'skills/category_detail.html', context)


@login_required
def skill_search_ajax(request):
    """AJAX search for skills"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    skills = Skill.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_active=True
    )[:10]
    
    results = [{
        'id': skill.id,
        'title': skill.title,
        'category': skill.category.name if skill.category else 'Uncategorized',
        'user': skill.user.username,
        'url': skill.get_absolute_url(),
    } for skill in skills]
    
    return JsonResponse({'results': results})
