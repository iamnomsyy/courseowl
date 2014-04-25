import os
from django.core.management import call_command
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.conf import settings
import haystack


TEST_INDEX = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'TIMEOUT': 60 * 10,
        'INDEX_NAME': 'test_index',
        'PATH': os.path.join(settings.BASE_DIR, 'test_index'),
    },
}

@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX)
class SearchTests(TestCase):
    fixtures = ['website/fixtures/courses.json']

    def setUp(self):
        self.c = Client()
        haystack.connections.reload('default')
        super(SearchTests, self).setUp()
        call_command('rebuild_index', interactive=False, verbosity=0)

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=0)

    def test_search_with_query(self):
        """
        Search any query: 
        the results page should include 'Results for' + that query
        """
        q = 'a query'
        response = self.c.get('/search/', {'q': q})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(('Results for ' + q) in response.content)

    def test_search_no_query(self):
        """
        Search for nothing: 
        the results page should include 'Results for' + that query
        """
        response = self.c.get('/search/', {})
        self.assertEquals(response.status_code, 200)
        self.assertTrue('To search, type something in the search box above.' in response.content)

    def test_search_course(self):
        """
        Search for the phrase 'computer':
        given the fixture, the course 'Intro to Computer Science' should come up
        """
        response = self.c.get('/search/', {'q': 'computer'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Intro to Computer Science' in response.content)

    def test_search_instructor(self):
        """
        Search for the phrase 'andrew ng':
        given the fixture, the course 'Machine Learning' should come up
        """
        response = self.c.get('/search/', {'q': 'andrew ng'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Machine Learning' in response.content)

    def test_search_provider(self):
        """
        Search for the phrase 'udacity':
        given the fixture, the course 'Artificial Intelligence for Robotics' should come up
        """
        response = self.c.get('/search/', {'q': 'udacity'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Artificial Intelligence for Robotics' in response.content)
