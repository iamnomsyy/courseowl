from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.test.client import Client
from django.http import HttpRequest, QueryDict
from accounts.views import *
from courses.models import *


class AccountsTest(TestCase):
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

    def test_valid_email(self):
        email1 = 'testmail.cu'
        email2 = 'testmail%$#.com'
        email3 = 'test@#.com'
        email4 = 'test@mail.com'

        self.assertFalse(valid_email_address(email1))
        self.assertFalse(valid_email_address(email2))
        self.assertFalse(valid_email_address(email3))
        self.assertTrue(valid_email_address(email4))

    def test_valid_password(self):
        tooshort = 'short'
        blank = ''
        valid = 'qwerty123'

        short = check_valid_password(tooshort, tooshort)
        none = check_valid_password(blank, blank)
        notmatching1 = check_valid_password(tooshort, 'blah')
        notmatching2 = check_valid_password(blank, 'asdf')
        validpw = check_valid_password(valid, valid)

        self.assertFalse(short)
        self.assertFalse(none)
        self.assertFalse(notmatching1)
        self.assertFalse(notmatching2)
        self.assertTrue(valid)

    def test_unique_user(self):
        email1 = 'test1@xyz.com'
        email2 = 'test2@xyz.com'
        password = 'qwerty123'
        user1 = User.objects.create_user(username_md5(email1), email1, password, first_name="", last_name="")

        user1_not_unique = unique_user(email1)
        user2_unique = unique_user(email2)
        self.assertFalse(user1_not_unique)
        self.assertTrue(user2_unique)

    def test_add_remove_course(self):
        user_profile = self.create_fake_userprofile()

        # postdata = urllib.urlencode({
        #     'course_to_add': 'Test course',
        #     'user': user_profile.user
        # })
        # req = urllib2.Request(
        #     url='/accounts/enroll',
        #     data=postdata
        # )
        self.client.login(username='abc@xyz.com', password='qwerty123')

        request = HttpRequest()
        request.POST = request.POST.copy()
        request.POST['course_to_add'] = 'Test course'
        request.user = user_profile.user
        request.method = 'POST'


        add_course(request)

        all_courses = list(user_profile.enrolled.all())
        self.assertEquals(len(all_courses), 1)

        the_course = all_courses[0]
        self.assertEquals(the_course.name, "Test course")
        self.assertEquals(the_course.description, "Test description")

        the_course = Course.objects.get(name='Test course')
        user_profile.enrolled.remove(the_course)
        user_profile.save()
        all_courses = list(user_profile.enrolled.all())
        self.assertEqual(len(all_courses), 0)