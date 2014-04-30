from django.test import TestCase
import json
import os
from bs4 import BeautifulSoup
from courses.recommender import get_fuzzy_subject_matching, get_enrolled_subjects, get_similar_user_interests, \
    get_similar_user_dislikes, get_recs_from_subjects, get_similar_user_completed
from courses.scripts.coursera import add_courses as coursera_add_courses
import courses.scripts.udacity as udacity
import courses.scripts.iversity as iversity
import courses.scripts.edx as edx
from courses.models import Subject, Provider, Course
from accounts.models import UserProfile, User

from courses.scripts.utilities import unify_subject_name


class SubjectTests(TestCase):
    def test_create_subject(self):
        """
        Creates a Subject model object and tests if it can be manipulated properly
        """
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
        """
        Load a json dict, then test if the course can be added correctly from the json data.
        """

        file_path = os.path.join(os.path.dirname(__file__), 'testCourse.json')

        with open(file_path) as f:
            json_dict = json.loads(f.read())
            coursera_add_courses(json_dict)

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
            self.assertEquals(the_course_subjects[1].name, 'cs')


class UdacityScriptTests(TestCase):
    def test_get_urls(self):
        """
        Tests if get_urls() returns a non empty list
        """
        l = udacity.get_urls()
        self.assertTrue(len(l) > 0)

    def test_get_all_courses(self):
        """
        Tests if we can get all courses properly
        """
        urls = ['https://www.udacity.com/course/cs046']
        all_courses = udacity.get_all_courses(urls)
        itp = all_courses['Intro to Programming']  # itp for 'Intro to Programming'
        self.assertEquals(itp['name'], 'Intro to Programming')
        self.assertEquals(itp['instr'], 'Cay Horstmann')
        self.assertEquals(itp['desc'].strip(), 'In this class, you will learn basic skills and concepts of computer programming in an object-oriented approach using Java.')
        # rationale for .strip(): scraper gets white space that doesn't affect display but gets in the way of testing
        self.assertEquals(len(itp['subj']), 0)


class EdxScriptTests(TestCase):
    def test_populate_lists(self):
        """
        Tests if lists are properly populated
        """
        edx.populate_lists(['business-management'])
        self.assertEquals(len(edx.all_subjects), 25)
        self.assertTrue('The Analytics Edge' in edx.title_list)

    def test_add_to_django(self):
        """
        Test if data from lists are properly added to Django database
        """
        edx.populate_lists(['business-management'])
        edx.add_to_django()
        edge_course = Course.objects.filter(name='The Analytics Edge')
        self.assertTrue(edge_course.exists())


class RecommenderTestsNormalCase(TestCase):
    def setUp(self):
        # Create three fake users and two fake courses
        self.subject_math = Subject()
        self.subject_math.name = 'math'
        self.subject_math.save()

        self.subject_english = Subject()
        self.subject_english.name = 'english'
        self.subject_english.save()

        self.subject_math2 = Subject()
        self.subject_math2.name = 'math-calculus'
        self.subject_math2.save()

        self.course_math = Course()
        self.course_math.name = 'intro to math'
        self.course_math.description = 'this is a introduction to math'
        self.course_math.save()
        self.course_math.subjects.add(self.subject_math)
        self.course_math.save()

        self.course_english = Course()
        self.course_english.name = 'Literature 100'
        self.course_english.description = 'Learn how to read!'
        self.course_english.save()
        self.course_english.subjects.add(self.subject_english)
        self.course_english.save()

        self.user1 = User.objects.create(username='user1')
        self.user_profile_1 = UserProfile.objects.create(user=self.user1)
        self.user_profile_1.save()
        self.user_profile_1.interests.add(self.subject_math2)
        self.user_profile_1.disliked.add(self.course_math)
        self.user_profile_1.disliked.add(self.course_english)
        self.user_profile_1.completed.add(self.course_math)
        self.user_profile_1.completed.add(self.course_english)
        self.user_profile_1.save()

        self.user_2 = User.objects.create(username='user2')
        self.user_profile_2 = UserProfile.objects.create(user=self.user_2)
        self.user_profile_2.save()
        self.user_profile_2.interests.add(self.subject_math2)
        self.user_profile_2.disliked.add(self.course_english)
        self.user_profile_2.disliked.add(self.course_math)
        self.user_profile_2.save()

        self.user_3 = User.objects.create(username='user3')
        self.user_profile_3 = UserProfile.objects.create(user=self.user_3)
        self.user_profile_3.save()
        self.user_profile_3.interests.add(self.subject_english)
        self.user_profile_3.disliked.add(self.course_math)
        self.user_profile_3.completed.add(self.course_math)
        self.user_profile_3.completed.add(self.course_english)
        self.user_profile_3.save()

    def test_fuzzy_matching_subject(self):
        subject_math3 = Subject()
        subject_math3.name = "math-algebra"
        subject_math3.save()

        subject_set = get_fuzzy_subject_matching(subject_math3)
        self.assertEqual(len(subject_set), 3)

    def test_get_recs_from_subjects(self):
        test_subs = set()
        test_subs.add(Subject.objects.get(name="math-calculus"))
        subject_set = get_recs_from_subjects(test_subs)
        self.assertEqual(len(subject_set), 1)
        self.assertEqual(subject_set.pop().name, "intro to math")

    def test_get_enrolled_subjects(self):
        self.assertEqual(len(get_enrolled_subjects(self.user1)), 2)

    def test_get_similar_user_interests(self):
        similar_user, numb = get_similar_user_interests(self.user1)
        self.assertEqual(similar_user, self.user_profile_2)
        self.assertEqual(numb, 1)

    def test_get_similar_user_dislikes(self):
        similar_user, numb = get_similar_user_dislikes(self.user1)
        self.assertEqual(similar_user, self.user_profile_2)
        self.assertEqual(numb, 2)

    def test_get_similar_user_completed(self):
        similar_user, numb = get_similar_user_completed(self.user1)
        print similar_user.user.username
        self.assertEqual(similar_user, self.user_profile_3)
        self.assertEqual(numb, 2)


class IversityScriptTests(TestCase):
    def test_add_to_django(self):
        """
        Tests if we can properly add courses to Django and the database
        """
        provider, created = Provider.objects.get_or_create(name='iversity')
        sample_div = "<article class='courses-list-item'><div class='ribbon-content'>Engineering</div></div><div class='course-body'><header><h2 class='truncate'><a href='https://iversity.org/courses/vehicle-dynamics-i-accelerating-and-braking'>Vehicle Dynamics I: Accelerating and Braking</a></h2><p class='instructors truncate'>Univ.-Prof. Dr.-Ing. Martin Meywerk</p></header><p class='description'>From Bugatti Veyron to Volkswagen Beetle, from racing to passenger car: study about their acceleration and braking and learn from two applications from automotive mechatronics. </p></div></div></div></div></div></div></div></article>"
        sample_div = BeautifulSoup(sample_div)
        iversity.create_course(sample_div, provider)

        # Make sure the Engineering subject was created:
        new_subject = Subject.objects.get(name='engineering')
        self.assertIsNotNone(new_subject)

        # Make sure the course itself was created:
        new_course = Course.objects.get(name='Vehicle Dynamics I: Accelerating and Braking', provider=provider,
                                        subjects=new_subject)
        self.assertIsNotNone(new_course)

        # Make sure the course name is set properly:
        self.assertEqual('Vehicle Dynamics I: Accelerating and Braking', new_course.name)

        # Make sure the course URL is set properly:
        self.assertEqual('https://iversity.org/courses/vehicle-dynamics-i-accelerating-and-braking', new_course.url)

        # Make sure the course instructor is set properly:
        self.assertEqual('Univ.-Prof. Dr.-Ing. Martin Meywerk', new_course.instructor)

        # Make sure the course description is set properly:
        self.assertEqual('From Bugatti Veyron to Volkswagen Beetle, from racing to passenger car: study about their acceleration and braking and learn from two applications from automotive mechatronics.', new_course.description)


class UnifySubjectNameTests(TestCase):
    def test_unify_subject_names(self):
        """
        Test if we properly get the first word from a subject
        """
        name_1 = 'cs-ai'
        name_2 = 'social science'
        name_3 = 'physical-education stuff'
        name_4 = 'beatles pop-song'
        self.assertEqual(unify_subject_name(name_1), 'cs')
        self.assertEqual(unify_subject_name(name_2), 'social')
        self.assertEqual(unify_subject_name(name_3), 'physical')
        self.assertEqual(unify_subject_name(name_4), 'beatles')

