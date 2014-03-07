import json

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from accounts.models import UserProfile
from courses.models import Subject, Course


def json_subjects(request):
    subject_arr = []
    for subject in Subject.objects.all():
        subject_arr.append(subject.name)
    return HttpResponse(json.dumps(subject_arr), mimetype='application/json')


def json_courses(request):
    course_arr = []
    for course in Course.objects.all():
        course_arr.append(course.name)
    return HttpResponse(json.dumps(course_arr), mimetype='application/json')


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
    return HttpResponse(json.dumps(enrolled_arr), mimetype='application/json')

def add_course(request):
    if request.method == "POST":
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            course_to_add = request.POST.get('course_to_add')
            the_course = Course.objects.get(name=course_to_add)
            user_profile.enrolled.add(the_course)
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, 'Course added successfully!')
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Course does not exist! Should never happen')
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


def drop_course(request):
    if request.method == "POST":
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            course_to_drop = request.POST.get('course_to_drop')
            the_course = Course.objects.get(name=course_to_drop)
            user_profile.enrolled.remove(the_course)
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, 'Course dropped successfully!')
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Error deleting course!')
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')
