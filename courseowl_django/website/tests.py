from django.test import TestCase, Client


class SearchTests(TestCase):
    fixtures = ['courses.json']

    def setUp(self):
        self.c = Client()

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

    # def test_search_course(self):
    #     """
    #     Search for the phrase 'computer':
    #     given the fixture, the course 'Intro to Computer Science' should come up
    #     """
    #     response = self.c.get('/search/', {'q': 'computer'})
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTrue('Intro to Computer Science' in response.content)

    # def test_search_instructor(self):
    #     """
    #     Search for the phrase 'andrew ng':
    #     given the fixture, the course 'Machine Learning' should come up
    #     """
    #     response = self.c.get('/search/', {'q': 'andrew ng'})
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTrue('Machine Learning' in response.content)

    # def test_search_provider(self):
    #     """
    #     Search for the phrase 'udacity':
    #     given the fixture, the course 'Artificial Intelligence for Robotics' should come up
    #     """
    #     response = self.c.get('/search/', {'q': 'udacity'})
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTrue('Artificial Intelligence for Robotics' in response.content)
        
