from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Subject, Course
from accounts.models import UserProfile
import json


def index(request):
    return render(request, 'website/index.html')


def error404(request):
    return render(request, 'website/error404.html')


@login_required
def subject_preferences(request):
    """
    On POST, save a user's subject preferences. On GET, generate all liked subjects and render the personalize page.
    """
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        subject_ids = json.loads(request.POST.get('subject_ids'))
        if user_profile.interests:
            # The subject preferences that we get from this page are definitive and not additive
            user_profile.interests.clear()
        # Save subjects to user's profile
        for sub_id in subject_ids:
            subject = Subject.objects.get(id=sub_id)
            user_profile.interests.add(subject)
        user_profile.save()
        return redirect('/course_preferences')

    liked_subjects = user_profile.interests.all()
    # Construct a flat list of ids to exclude from all subjects
    unliked = Subject.objects.exclude(id__in=liked_subjects.values_list('id', flat=True))
    context = {
        'liked_subjects': liked_subjects.order_by('name'),
        'subjects': unliked.order_by('name')
    }
    return render(request, 'website/personalize_subjects.html', context)


@login_required
def course_preferences(request):
    """
    On POST, save a user's course preferences. On GET, generate all liked courses and render the personalize page.
    """
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        course_ids = json.loads(request.POST.get('course_ids'))
        if user_profile.enrolled:
            user_profile.enrolled.clear()
        for course in course_ids:
            user_profile.enrolled.add(Course.objects.get(id=course))
        user_profile.save()
        return redirect('/accounts/profile/')

    liked_subjects = UserProfile.objects.get(user=request.user).interests.all()
    context = {
        'courses': Course.objects.filter(subjects__in=liked_subjects).distinct().order_by('name'),
        'enrolled': user_profile.enrolled.all().order_by('name')
    }
    return render(request, 'website/personalize_courses.html', context)