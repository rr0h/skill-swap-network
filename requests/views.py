from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import SkillRequest, RequestMessage
from .forms import SkillRequestForm, RequestMessageForm
from skills.models import Skill


@login_required
def request_list(request):
    """List all requests (sent and received)"""
    sent_requests = SkillRequest.objects.filter(sender=request.user).select_related('skill', 'receiver')
    received_requests = SkillRequest.objects.filter(receiver=request.user).select_related('skill', 'sender')
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        sent_requests = sent_requests.filter(status=status_filter)
        received_requests = received_requests.filter(status=status_filter)
    
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'status_filter': status_filter,
    }
    
    return render(request, 'requests/request_list.html', context)


@login_required
def request_create(request, skill_id):
    """Create a new skill request"""
    skill = get_object_or_404(Skill, pk=skill_id, is_active=True)
    
    # Check if user is trying to request their own skill
    if skill.user == request.user:
        messages.error(request, "You cannot request your own skill!")
        return redirect('skills:skill_detail', pk=skill_id)
    
    # Check if request already exists
    existing_request = SkillRequest.objects.filter(
        sender=request.user,
        skill=skill,
        status__in=['pending', 'accepted']
    ).first()
    
    if existing_request:
        messages.warning(request, "You already have a pending or accepted request for this skill!")
        return redirect('requests:request_detail', pk=existing_request.pk)
    
    if request.method == 'POST':
        form = SkillRequestForm(request.POST)
        if form.is_valid():
            skill_request = form.save(commit=False)
            skill_request.sender = request.user
            skill_request.receiver = skill.user
            skill_request.skill = skill
            skill_request.save()
            messages.success(request, 'Request sent successfully!')
            return redirect('requests:request_detail', pk=skill_request.pk)
    else:
        form = SkillRequestForm()
    
    context = {
        'form': form,
        'skill': skill,
    }
    
    return render(request, 'requests/request_create.html', context)


@login_required
def request_detail(request, pk):
    """View request details and messages"""
    skill_request = get_object_or_404(
        SkillRequest.objects.select_related('sender', 'receiver', 'skill'),
        pk=pk
    )
    
    # Check if user is part of this request
    if request.user not in [skill_request.sender, skill_request.receiver]:
        messages.error(request, "You don't have permission to view this request!")
        return redirect('requests:request_list')
    
    # Handle message submission
    if request.method == 'POST':
        message_form = RequestMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.request = skill_request
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent!')
            return redirect('requests:request_detail', pk=pk)
    else:
        message_form = RequestMessageForm()
    
    # Mark messages as read
    RequestMessage.objects.filter(
        request=skill_request
    ).exclude(sender=request.user).update(is_read=True)
    
    request_messages = skill_request.messages.all().select_related('sender')
    
    context = {
        'skill_request': skill_request,
        'messages': request_messages,
        'message_form': message_form,
        'is_sender': request.user == skill_request.sender,
        'is_receiver': request.user == skill_request.receiver,
    }
    
    return render(request, 'requests/request_detail.html', context)


@login_required
def request_accept(request, pk):
    """Accept a skill request"""
    skill_request = get_object_or_404(SkillRequest, pk=pk, receiver=request.user)
    
    if skill_request.can_accept():
        skill_request.status = 'accepted'
        skill_request.accepted_at = timezone.now()
        skill_request.save()
        messages.success(request, 'Request accepted!')
    else:
        messages.error(request, 'This request cannot be accepted!')
    
    return redirect('requests:request_detail', pk=pk)


@login_required
def request_reject(request, pk):
    """Reject a skill request"""
    skill_request = get_object_or_404(SkillRequest, pk=pk, receiver=request.user)
    
    if skill_request.can_reject():
        skill_request.status = 'rejected'
        skill_request.save()
        messages.success(request, 'Request rejected!')
    else:
        messages.error(request, 'This request cannot be rejected!')
    
    return redirect('requests:request_detail', pk=pk)


@login_required
def request_complete(request, pk):
    """Mark request as completed"""
    skill_request = get_object_or_404(SkillRequest, pk=pk)
    
    # Both sender and receiver can mark as complete
    if request.user not in [skill_request.sender, skill_request.receiver]:
        messages.error(request, "You don't have permission to complete this request!")
        return redirect('requests:request_list')
    
    if skill_request.can_complete():
        skill_request.status = 'completed'
        skill_request.completed_at = timezone.now()
        skill_request.save()
        messages.success(request, 'Request marked as completed! You can now leave a review.')
        return redirect('reviews:create_review', request_id=pk)
    else:
        messages.error(request, 'This request cannot be completed!')
    
    return redirect('requests:request_detail', pk=pk)


@login_required
def request_cancel(request, pk):
    """Cancel a skill request"""
    skill_request = get_object_or_404(SkillRequest, pk=pk, sender=request.user)
    
    if skill_request.can_cancel():
        skill_request.status = 'cancelled'
        skill_request.save()
        messages.success(request, 'Request cancelled!')
    else:
        messages.error(request, 'This request cannot be cancelled!')
    
    return redirect('requests:request_list')
