from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from skills.models import Skill, Category
from requests.models import SkillRequest
from reviews.models import Review
from users.models import UserSkill


@login_required
def dashboard_home(request):
    """Main dashboard view"""
    user = request.user
    
    # Get user statistics
    skills_offered_count = user.skills_offered.count()
    sent_requests_count = user.sent_requests.count()
    received_requests_count = user.received_requests.count()
    reviews_received_count = user.received_reviews.count()
    
    # Get pending requests
    pending_sent = user.sent_requests.filter(status='pending')[:5]
    pending_received = user.received_requests.filter(status='pending')[:5]
    
    # Get active requests
    active_requests = SkillRequest.objects.filter(
        Q(sender=user) | Q(receiver=user),
        status='accepted'
    )[:5]
    
    # Get recommended skills based on user interests
    user_skills_wanted = user.user_skills.filter(skill_type='want').values_list('skill_name', flat=True)
    recommended_skills = Skill.objects.filter(
        is_active=True
    ).exclude(user=user)
    
    if user_skills_wanted:
        recommended_skills = recommended_skills.filter(
            Q(title__icontains=user_skills_wanted[0]) if user_skills_wanted else Q()
        )
    
    recommended_skills = recommended_skills.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating', '-created_at')[:6]
    
    # Get all categories with skill counts
    categories = Category.objects.annotate(
        skill_count=Count('skills', filter=Q(skills__is_active=True))
    ).order_by('-skill_count')[:8]
    
    # Get recent reviews
    recent_reviews = user.received_reviews.all()[:5]
    
    # Activity data for chart
    activity_data = {
        'skills_offered': skills_offered_count,
        'requests_sent': sent_requests_count,
        'requests_received': received_requests_count,
        'reviews': reviews_received_count,
    }
    
    context = {
        'skills_offered_count': skills_offered_count,
        'sent_requests_count': sent_requests_count,
        'received_requests_count': received_requests_count,
        'reviews_received_count': reviews_received_count,
        'pending_sent': pending_sent,
        'pending_received': pending_received,
        'active_requests': active_requests,
        'recommended_skills': recommended_skills,
        'categories': categories,
        'recent_reviews': recent_reviews,
        'activity_data': activity_data,
        'average_rating': user.get_average_rating(),
        'profile_completion': user.get_profile_completion(),
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_stats(request):
    """User statistics view"""
    user = request.user
    
    # Get detailed statistics
    total_skills = user.skills_offered.count()
    total_requests_sent = user.sent_requests.count()
    total_requests_received = user.received_requests.count()
    
    # Request status breakdown
    requests_by_status = {
        'pending': user.sent_requests.filter(status='pending').count(),
        'accepted': user.sent_requests.filter(status='accepted').count(),
        'completed': user.sent_requests.filter(status='completed').count(),
        'rejected': user.sent_requests.filter(status='rejected').count(),
        'cancelled': user.sent_requests.filter(status='cancelled').count(),
    }
    
    # Reviews statistics
    reviews = user.received_reviews.all()
    total_reviews = reviews.count()
    average_rating = user.get_average_rating()
    
    rating_breakdown = {
        '5_star': reviews.filter(rating=5).count(),
        '4_star': reviews.filter(rating=4).count(),
        '3_star': reviews.filter(rating=3).count(),
        '2_star': reviews.filter(rating=2).count(),
        '1_star': reviews.filter(rating=1).count(),
    }
    
    # Most viewed skills
    popular_skills = user.skills_offered.order_by('-views_count')[:5]
    
    context = {
        'total_skills': total_skills,
        'total_requests_sent': total_requests_sent,
        'total_requests_received': total_requests_received,
        'requests_by_status': requests_by_status,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'rating_breakdown': rating_breakdown,
        'popular_skills': popular_skills,
    }
    
    return render(request, 'dashboard/stats.html', context)
