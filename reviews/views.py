from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from requests.models import SkillRequest
from users.models import User


@login_required
def create_review(request, request_id):
    """Create a review for a completed request"""
    skill_request = get_object_or_404(SkillRequest, pk=request_id, status='completed')
    
    # Check if user is part of this request
    if request.user not in [skill_request.sender, skill_request.receiver]:
        messages.error(request, "You don't have permission to review this request!")
        return redirect('requests:request_list')
    
    # Check if review already exists
    if hasattr(skill_request, 'review') and skill_request.review.reviewer == request.user:
        messages.warning(request, "You have already reviewed this exchange!")
        return redirect('requests:request_detail', pk=request_id)
    
    # Determine who is being reviewed
    reviewed_user = skill_request.receiver if request.user == skill_request.sender else skill_request.sender
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.skill = skill_request.skill
            review.request = skill_request
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('users:profile', username=reviewed_user.username)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'skill_request': skill_request,
        'reviewed_user': reviewed_user,
    }
    
    return render(request, 'reviews/create_review.html', context)


@login_required
def user_reviews(request, username):
    """View all reviews for a user"""
    user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(reviewed_user=user).select_related('reviewer', 'skill')
    
    context = {
        'profile_user': user,
        'reviews': reviews,
        'average_rating': user.get_average_rating(),
        'total_reviews': user.get_total_reviews(),
    }
    
    return render(request, 'reviews/user_reviews.html', context)


@login_required
def skill_reviews(request, skill_id):
    """View all reviews for a skill"""
    from skills.models import Skill
    skill = get_object_or_404(Skill, pk=skill_id)
    reviews = Review.objects.filter(skill=skill).select_related('reviewer', 'reviewed_user')
    
    context = {
        'skill': skill,
        'reviews': reviews,
    }
    
    return render(request, 'reviews/skill_reviews.html', context)
