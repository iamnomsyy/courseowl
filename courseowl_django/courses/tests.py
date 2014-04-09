from django.test import TestCase
from courses.models import Subject, Provider, Source, Course
import json
import os

from courses.scripts.coursera import addCourses as courseraAddCourses
import courses.scripts.udacity as udacity
import scripts.edx as edx


class SubjectTests(TestCase):
    def test_create_subject(self):
        subject = Subject()
        subject.name = 'CS'
        subject.save()

        all_subjects = Subject.objects.all()

        self.assertEquals(len(all_subjects), 1)
        only_subject = all_subjects[0]
        self.assertEquals(only_subject, subject)

        self.assertEquals(only_subject.name, 'CS')

class CourseraScriptTests(TestCase):
    def test_add_course(self):
        '''
        Load a json dict, then test if the course can be added correctly from the json data.
        '''

        filePath = os.path.join(os.path.dirname(__file__), 'testCourse.json')

        with open(filePath) as f:
            jsonDict = json.loads(f.read())
            courseraAddCourses(jsonDict)

            # there is one course in the test file
            all_courses = Course.objects.all()
            self.assertEquals(len(all_courses), 1)

            # the course has the right attributes
            the_course = all_courses[0]
            self.assertEquals(the_course.name, 'Machine Learning')
            self.assertEquals(the_course.description, 'Learn about the most effective machine learning techniques, and gain practice implementing them and getting them to work for yourself.')
            self.assertEquals(the_course.instructor, 'Andrew Ng, Associate Professor')

            # the course has the right university
            self.assertEquals(the_course.source.name, 'Stanford University')

            # the course has the right subjects
            the_course_subjects = the_course.subjects.all()
            self.assertEquals(len(the_course_subjects), 2)
            self.assertEquals(the_course_subjects[0].name, 'stats')
            self.assertEquals(the_course_subjects[1].name, 'cs-ai')

class UdacityScriptTests(TestCase):
    def test_get_urls(self):
        l = udacity.get_urls()
        self.assertTrue(len(l) > 0)

    def test_get_all_courses(self):
        urls = ['https://www.udacity.com/course/cs046']
        all_courses = udacity.get_all_courses(urls)
        itp = all_courses['Intro to Programming'] # itp for 'Intro to Programming'
        self.assertEquals(itp['name'], 'Intro to Programming')
        self.assertEquals(itp['instr'], 'Cay Horstmann')
        self.assertEquals(itp['desc'].strip(), 'In this class, you will learn basic skills and concepts of computer programming in an object-oriented approach using Java.')
        # rationale for .strip(): scraper gets white space that doesn't affect display but gets in the way of testing
        self.assertEquals(len(itp['subj']), 0)

class EdxScriptTests(TestCase):
    def test_populate_lists(self):
        edx.populate_lists()
        self.assertEquals(len(edx.subjects), 25)
        self.assertTrue(len(edx.titleList) > 50)
        self.assertEquals(len(edx.titleList), len(edx.descList))
        self.assertEqual(len(edx.titleList), len(edx.intList))
        self.assertEqual(len(edx.titleList), len(edx.uniList))

    def test_add_to_django(self):
        edx.populate_lists()
        edx.add_to_django()
        self.assertTrue(len(list(Course.objects.all())) > 50)
        self.assertEquals(len(list(Subject.objects.all())), 25)

class RecommenderTests(TestCase):
    math_sub = Subject()
    sic_sub = Sect()






