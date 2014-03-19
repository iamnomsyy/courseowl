from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Subject, Course
from accounts.models import UserProfile
import json


def index(request):
    return render(request, 'website/index.html')


@login_required
def subject_preferences(request):
    if request.method == 'POST':
        subject_ids = json.loads(request.POST.get('subject_ids'))
        # Save subjects to user's profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if created:
            user_profile.save()
        for sub_id in subject_ids:
            subject = Subject.objects.get(id=sub_id)
            interests = user_profile.interests.add(subject)
        user_profile.save()
        return redirect('/course_preferences')

    context = {'subjects': Subject.objects.all().extra(order_by=['name'])}
    return render(request, 'website/personalize_subjects.html', context)


@login_required
def course_preferences(request):
    if request.method == 'POST':
        course_ids = json.loads(request.POST.get('course_ids'))
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        for course in course_ids:
            user_profile.enrolled.add(Course.objects.get(id=course))
        user_profile.save()
        return redirect('/accounts/profile')

    liked_subjects = UserProfile.objects.get(user=request.user).interests.all()
    context = {'courses': Course.objects.filter(subjects__in=liked_subjects)}
    return render(request, 'website/personalize_courses.html', context)