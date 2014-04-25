import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
        subject_id = request.POST.get('liked_subject')
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            user_profile.interests.add(Subject.objects.get(id=subject_id))
        except:
            success = False
        return HttpResponse(json.dumps({'success': success}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@login_required
def dislike_course(request):
    """
    POST here when you dislike a course with a 'disliked_course' data property.
    Method: POST, {'disliked_course': 'name of course'}
    """
    if request.method == 'POST':
        success = True
        course_id = request.POST.get('disliked_course')
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            user_profile.disliked.add(Course.objects.get(id=course_id))
        except:
            success = False
        return HttpResponse(json.dumps({'success': success}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@login_required
def complete_course(request):
    """
    POST here when you complete a course with a 'completed_course' data property.
    Method: POST, {'completed_course': 'name of course'}
    """
    if request.method == 'POST':
        success = True
        course_id = request.POST.get('completed_course')
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            user_profile.completed.add(Course.objects.get(id=course_id))
        except:
            success = False
        return HttpResponse(json.dumps({'success': success}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


def json_random_courses(request):
    """
    Returns courses that are random for now, but will eventually be recommendations.
    """
    random_courses = []
    if request.method == 'POST':
        rand_course_order = Course.objects.order_by('?')
        num_rand_courses = 5
        for i in range(num_rand_courses):
            random_courses.append(rand_course_order[i])  # append here since rand_course_order is a query, not a list
    return HttpResponse(json.dumps(random_courses), mimetype='application/json')


@login_required
def add_course(request):
    if request.method == "POST":
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            course_to_add = request.POST.get('course_to_add')
            the_course = Course.objects.get(id=course_to_add)
            user_profile.enrolled.add(the_course)
            user_profile.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@login_required
def drop_course(request):
    """
    Drops a course from the user
    """
    if request.method == "POST":
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            course_to_drop = request.POST.get('course_to_drop')
            the_course = Course.objects.get(id=course_to_drop)
            user_profile.enrolled.remove(the_course)
            user_profile.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


def get_similar_courses(course):
    """
    given a Course, return a list of 3 Courses that are similar
    """
    subject = course.subjects.all()[0]
    return Course.objects.filter(subjects__name=subject.name).exclude(id=course.id)[:3]


@login_required
def course_info(request):
    """
    Returns a JSON dump of the information of a course given its courseID
    Method: POST, {'course_id': courseID#}
    """
    if request.method == "POST":
        try:
            course_id = request.POST.get('course_id')
            the_course = Course.objects.get(id=course_id)
            helpout_url = 'https://helpouts.google.com/search?q='

            for word in the_course.name.split(' '):
                helpout_url += word + '%20OR%20'
            helpout_url = helpout_url[:-8]  # cutting off the last %20OR%20

            subject_list = [subj.name.capitalize() for subj in the_course.subjects.all()]
            similar_courses = get_similar_courses(the_course)

            similar_courses_names = [course.name for course in similar_courses]
            similar_courses_links = [course.url for course in similar_courses]

            course_data = {'description': the_course.description, 'provider': the_course.provider.name,
                           'subjects': subject_list, 'instructor': the_course.instructor,
                           'name': the_course.name, 'url': the_course.url,
                           'similar_courses_names': similar_courses_names,
                           'similar_courses_links': similar_courses_links,
                           'helpouturl': helpout_url
            }

            return HttpResponse(json.dumps({'success': True, 'info': course_data}), content_type='application/json')
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')
