from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client
import json
from api.views import add_course, drop_course, get_similar_courses
from courses.models import Provider, Subject, Course
from accounts.models import UserProfile, User
from accounts.views import username_md5


class TestAPI(TestCase):
    def setUp(self):
        """
        Set up a test user and user profile
        """
        self.client = Client()
        self.user = User.objects.create_user(username='bob12345', email='bob@bob.com', password='bob123456',
                                             first_name='', last_name='')
        self.user_profile = UserProfile.objects.create(user=self.user)

        # to avoid conflict with a test written before this setup
        # append '2' to provider and subject names
        self.test_provider = Provider(name='Test provider 2')
        self.test_provider.save()
        self.test_subject = Subject(name='Test subject 2')
        self.test_subject.save()

        self.test_course_1 = Course(name='Pottery 1', description="Test description 1", provider=self.test_provider,
                                    instructor="Test instructor 1", url='http://www.example.com/1')
        self.test_course_1.save()
        self.test_course_1.subjects.add(self.test_subject)
        self.test_course_1.save()

        self.test_course_2 = Course(name='Pottery 2', description="Test description 2", provider=self.test_provider,
                                    instructor="Test instructor 2", url='http://www.example.com/2')
        self.test_course_2.save()
        self.test_course_2.subjects.add(self.test_subject)
        self.test_course_2.save()

        self.test_course_3 = Course(name='Pottery 3', description="Test description 3", provider=self.test_provider,
                                    instructor="Test instructor 3", url='http://www.example.com/3')
        self.test_course_3.save()
        self.test_course_3.subjects.add(self.test_subject)
        self.test_course_3.save()

    def test_json_subjects(self):
        """
        Test the /api/subjects/ endpoint
        """
        temp_subject = Subject(name='Pottery')
        temp_subject.save()

        response = self.client.get('/api/subjects/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Pottery' in response.content)

    def test_json_courses(self):
        """
        Test the /api/courses/ endpoint
        """
        temp_course = Course(name='Advanced Pottery III')
        temp_course.save()

        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Advanced Pottery III' in response.content)

    def test_json_enrolled_courses(self):
        """
        Test the /api/enrolled_courses/ endpoint for a logged in user
        """
        temp_course = Course(name='Advanced Pottery III', description='Learn pottery like you never imagined possible.',
                             instructor='Bob Smith')
        temp_course.save()

        self.user_profile.enrolled.add(temp_course)
        self.user_profile.save()

        login_successful = self.client.login(username='bob12345', password='bob123456')
        self.assertTrue(login_successful)

        response = self.client.get('/api/enrolled_courses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('["Advanced Pottery III"]', response.content)

    def test_json_liked_subjects(self):
        """
        Test the /api/liked_subjects/ endpoint for a logged in user
        """
        temp_subject = Subject(name='Computer Science')
        temp_subject.save()

        temp_subject_two = Subject(name='Computer Engineering')
        temp_subject_two.save()

        self.user_profile.interests.add(temp_subject)
        self.user_profile.interests.add(temp_subject_two)
        self.user_profile.save()

        login_successful = self.client.login(username='bob12345', password='bob123456')
        self.assertTrue(login_successful)
        response = self.client.get('/api/liked_subjects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('["Computer Science", "Computer Engineering"]', response.content)

    def test_json_like_subject(self):
        """
        Test the /api/like_subject/ endpoint for a logged in user
        """
        login_successful = self.client.login(username='bob12345', password='bob123456')
        self.assertTrue(login_successful)

        temp_subject = Subject(name='Pottery')
        temp_subject.save()
        response = self.client.post('/api/like_subject/', data={'liked_subject': temp_subject.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"success": true}', response.content)
        response = self.client.post('/api/like_subject/', data={'liked_subject': 1234567890})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"success": false}', response.content)

    def test_json_dislike_course(self):
        """
        Test the /api/dislike_course/ endpoint for a logged in user
        """
        login_successful = self.client.login(username='bob12345', password='bob123456')
        self.assertTrue(login_successful)

        temp_course = Course(name='Pottery')
        temp_course.save()
        response = self.client.post('/api/dislike_course/', data={'disliked_course': temp_course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"success": true}', response.content)
        response = self.client.post('/api/dislike_course/', data={'disliked_course': 1234567890})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"success": false}', response.content)

    def test_json_complete_course(self):
        """
        Test the /api/complete_course/ endpoint for a logged in user
        """
        login_successful = self.client.login(username='bob12345', password='bob123456')
        self.assertTrue(login_successful)

        temp_course = Course(name='Pottery')
        temp_course.save()
        response = self.client.post('/api/complete_course/', data={'completed_course': temp_course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"success": true}', response.content)
        response = self.client.post('/api/complete_course/', data={'completed_course': 1234567890})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"success": false}', response.content)

    def create_fake_userprofile(self):
        """
        Helper function to create a fake user profile for tests
        """
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
        """
        Test the /api/remove_course/ endpoint for a logged in user
        """
        user_profile = self.create_fake_userprofile()
        self.client.login(username='abc@xyz.com', password='qwerty123')

        test_course = Course.objects.get(name="Test course")

        request = HttpRequest()
        request.POST['course_to_add'] = test_course.id
        request.user = user_profile.user
        request.method = 'POST'

        add_course(request)

        all_courses = list(user_profile.enrolled.all())
        self.assertEquals(len(all_courses), 1)

        the_course = all_courses[0]
        self.assertEquals(the_course.name, test_course.name)
        self.assertEquals(the_course.description, test_course.description)

        request.POST['course_to_drop'] = the_course.id
        drop_course(request)

        all_courses = list(user_profile.enrolled.all())
        self.assertEqual(len(all_courses), 0)

    def test_course_info(self):
        """
        Test the /api/course_info/ endpoint for a logged in user
        """
        login_successful = self.client.login(username='bob12345', password='bob123456')
        self.assertTrue(login_successful)

        temp_provider = Provider(name='Test provider')
        temp_provider.save()
        temp_subject = Subject(name='Test subject')
        temp_subject.save()
        temp_course = Course(name='Pottery', description="Test description", provider=temp_provider,
                             instructor="Test instructor")
        temp_course.save()
        temp_course.subjects.add(temp_subject)
        temp_course.save()

        helpout_url = 'https://helpouts.google.com/search?q='

        for word in temp_course.name.split(' '):
            helpout_url += word + '%20OR%20'
        helpout_url = helpout_url[:-8]  # remove trailing %20OR%20

        course_info = {'description': 'Test description', 'provider': 'Test provider',
                       'instructor': 'Test instructor', 'name': 'Pottery', 'url': '',
                       'subjects': ['Test subject'], 'helpouturl': helpout_url,
                       'similar_courses_names': [], 'similar_courses_links': []}
        expected_content = {'success': True, 'info': course_info}

        response = self.client.post('/api/course_info/', data={'course_id': temp_course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(expected_content), response.content)

        response = self.client.post('/api/complete_course/', data={'course_id': 1234567890})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"success": false}', response.content)

    def test_similar_courses(self):
        """
        Test the /api/similar_courses/ endpoint for a logged in user
        """
        similar_courses = get_similar_courses(self.test_course_1)
        self.assertEqual(len(similar_courses), 2)
        self.assertIn(self.test_course_2, similar_courses)
        self.assertIn(self.test_course_3, similar_courses)
