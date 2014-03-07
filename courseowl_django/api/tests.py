from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test.client import Client
from django.test import TestCase

from api.views import *
from courses.models import *
from accounts.views import *


class ApiTests(TestCase):
    def setUp(self):
            self.client = Client()

    def create_fake_userprofile(self):
        email = "abc@xyz.com"
        password = "qwerty123"
        user = User.objects.create_user(username_md5(email), email, password, first_name="", last_name="")
        user.save()
        user_profile = UserProfile(user=user)

        course_name = "Test course"
        description = "Test description"
        c, created = Course.objects.get_or_create(name=course_name, description=description, instructor='instructor')

        user_profile.save()
        user_profile.enrolled.add(c)
        user_profile.save()
        return user_profile

    def test_add_remove_course(self):
        user_profile = self.create_fake_userprofile()
        self.client.login(username='abc@xyz.com', password='qwerty123')

        request = HttpRequest()
        request.POST = request.POST.copy()
        request.POST['course_to_add'] = 'Test course'
        request.user = user_profile.user
        request.method = 'POST'

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        add_course(request)

        all_courses = list(user_profile.enrolled.all())
        self.assertEquals(len(all_courses), 1)

        the_course = all_courses[0]
        self.assertEquals(the_course.name, "Test course")
        self.assertEquals(the_course.description, "Test description")

        request.POST['course_to_drop'] = 'Test course'
        drop_course(request)

        all_courses = list(user_profile.enrolled.all())
        self.assertEqual(len(all_courses), 0)