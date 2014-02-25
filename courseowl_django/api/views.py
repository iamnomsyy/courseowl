import json
from django.http import HttpResponse
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
