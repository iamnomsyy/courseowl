from django.test import TestCase, Client

class SearchTests(TestCase):
    def test_search_course(self):
        c = Client()
        response = c.get('/search/', {'q': 'computer'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Intro to Computer Science' in response.content)