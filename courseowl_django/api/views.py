import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserProfile
from courses.models import Subject, Course


def json_subjects(request):
    subject_arr = []
    for subject in Subject.objects.all():
        subject_arr.append(subject.name)
    return HttpResponse(json.dumps(subject_arr))


def json_courses(request):
    course_arr = []
    for course in Course.objects.all():
        course_arr.append(course.name)
    return HttpResponse(json.dumps(course_arr))


@login_required
def json_enrolled_courses(request):
    """
    Return a JSON array of courses that request.user is signed up for (make a POST request).
    """
    enrolled_arr = []
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)

        for course in user_profile.enrolled.objects.all():
            enrolled_arr.append(course.name)
    return HttpResponse(json.dumps(enrolled_arr))
