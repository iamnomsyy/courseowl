from django.test import TestCase
from django.test.client import Client
from courses.models import Subject, Course


class TestAPI(TestCase):
    def setUp(self):
        self.client = Client()

    def test_json_subjects(self):
        temp_subject = Subject(name='Pottery')
        temp_subject.save()
        response = self.client.get('/api/subjects')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Pottery' in response.content)

    def test_json_courses(self):
        temp_course = Course(name='Advanced Pottery III')
        temp_course.save()
        response = self.client.get('/api/courses')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Advanced Pottery III' in response.content)

    def test_json_enrolled_courses(self):
        pass  # TODO once Erik and David get the framework for this set up

    def test_json_liked_subject(self):
        pass  # TODO once Erik and David get the framework for this set up

    def test_json_like_subject(self):
        pass  # TODO once Erik and David get the framework for this set up
