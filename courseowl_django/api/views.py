import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from courses.models import Subject, Course


def json_subjects(request):
    """
    Return a JSON array of all the subjects in the CourseOwl database.
    Method: GET
    """
    subject_arr = []
    for subject in Subject.objects.all():
        subject_arr.append(subject.name)
    return HttpResponse(json.dumps(subject_arr), content_type='application/json')


def json_courses(request):
    """
    Return a JSON array of all the courses in the CourseOwl database.
    Method: GET
    """
    course_arr = []
    for course in Course.objects.all():
        course_arr.append(course.name)
    return HttpResponse(json.dumps(course_arr), content_type='application/json')


@login_required
def json_enrolled_courses(request):
    """
    Return a JSON array of courses that request.user is signed up for.
    Method: GET
    """
    enrolled_arr = []
    user_profile = UserProfile.objects.get(user=request.user)

    for course in user_profile.enrolled.all():
        enrolled_arr.append(course.name)
    return HttpResponse(json.dumps(enrolled_arr), content_type='application/json')


@login_required
def json_liked_subjects(request):
    """
    Return a JSON array of courses that request.user has liked.
    Method: GET
    """
    liked_arr = []
    user_profile = UserProfile.objects.get(user=request.user)

    for subject in user_profile.interests.all():
        liked_arr.append(subject.name)
    return HttpResponse(json.dumps(liked_arr), content_type='application/json')


@login_required
def like_subject(request):
    """
    POST here when you like a subject with a 'liked_subject' data property.
    Method: POST, {'liked_subject': 'name of subject'}
    """
    if request.method == 'POST':
        success = True
        subject_name = request.POST.get('liked_subject')
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            user_profile.interests.add(Subject.objects.get(name=subject_name))
        except:
            success = False
        return HttpResponse(json.dumps({'success': success}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


def sample_courses_for_subject(request):
    """
    POST here with 'subject' to get 3 sample courses and all their information back.
    Method: POST, {"subject": "name of subject"}
    Returns: {"Course name": ["course description", "course provider"], "2nd course name": ["2nd desc"...
    """
    sample_courses = {}
    if request.method == 'POST':
        subject_name = request.POST.get('subject')
        try:
            subject_obj = Subject.objects.get(name=subject_name)
        except:
            return HttpResponse(json.dumps({}), content_type='application/json')
        sample_course_list = list(Course.objects.filter(subjects=subject_obj))
        for i in range(0, 3):
            sample_courses[sample_course_list[i].name] = [sample_course_list[i].description, sample_course_list[i].provider]
    return HttpResponse(json.dumps(sample_courses), content_type='application/json')
