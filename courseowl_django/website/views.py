from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Subject, Course
from accounts.models import UserProfile
import json


def index(request):
    return render(request, 'website/index.html')


@login_required
def subject_preferences(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        user_profile.save()

    if request.method == 'POST':
        subject_ids = json.loads(request.POST.get('subject_ids'))
        if user_profile.interests:
            # The subject preferences that we get from this page are definitive and not additive
            user_profile.interests.clear()
        # Save subjects to user's profile
        for sub_id in subject_ids:
            subject = Subject.objects.get(id=sub_id)
            interests = user_profile.interests.add(subject)
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
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        course_ids = json.loads(request.POST.get('course_ids'))
        if user_profile.enrolled:
            user_profile.enrolled.clear()
        for course in course_ids:
            user_profile.enrolled.add(Course.objects.get(id=course))
        user_profile.save()
        return redirect('/accounts/profile')

    liked_subjects = user_profile.interests.all()
    enrolled_courses = user_profile.enrolled.all()
    # Get courses in liked subjects that the user is not enrolled in already
    other_courses = Course.objects.filter(subjects__in=liked_subjects).exclude(id__in=enrolled_courses.values_list('id', flat=True))
    context = {
        'courses': other_courses.order_by('name'),
        'enrolled': enrolled_courses.order_by('name')
    }
    return render(request, 'website/personalize_courses.html', context)


def search(request):
    query = request.GET.get('query')
    
    # test data for iteration 2
    courses = [ {'name': 'Introduction to Programming', 
                 'prov': 'Coursera',
                 'instr': 'J. Random Teacher I',
                 'src': 'Stanford'},
                 {'name': 'Introduction to Statistics', 
                 'prov': 'Coursera',
                 'instr': 'J. Random Teacher II',
                 'src': 'MIT'},
                 {'name': 'Introduction to AI', 
                 'prov': 'Udacity',
                 'instr': 'J. Random Teacher III',
                 'src': 'UC Berkeley'},
                 {'name': 'Introduction to Bagels', 
                 'prov': 'EdX',
                 'instr': 'J. Random Teacher I',
                 'src': 'Google'},
                 {'name': 'Introduction to Google', 
                 'prov': 'EdX',
                 'instr': 'J. Random Teacher I',
                 'src': 'Microsoft'},
              ]

    context = {'query': query, 'courses': courses}
    return render(request, 'website/search.html', context)
