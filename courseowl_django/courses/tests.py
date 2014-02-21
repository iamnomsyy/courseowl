from django.test import TestCase
from courses.models import Subject, Provider, Source, Course
import json
import os

from courses.scripts.coursera import addCourses as courseraAddCourses

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

class ScriptTests(TestCase):
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


