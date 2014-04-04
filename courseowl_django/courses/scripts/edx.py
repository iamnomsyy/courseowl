from ..models import *
import urllib2
from bs4 import BeautifulSoup
import re


all_subjects = [
    'business-management',
    'chemistry',
    'communication',
    'computer-science',
    'economics-finance',
    'electronics',
    'energy-earth-sciences',
    'engineering',
    'environmental-studies',
    'food-nutrition',
    'health-safety',
    'history',
    'humanities',
    'law',
    'literature',
    'math',
    'medicine',
    'music',
    'philanthropy',
    'philosophy-ethics',
    'physics',
    'science',
    'social-sciences',
    'biology-life-sciences',
    'statistics-data-analysis'
]

int_list = list()
uni_list = list()
title_list = list()
desc_list = list()
sub_list = list()


def run():
    populate_lists()
    add_to_django()


def populate_lists(subject_list=None):
    print("Adding courses from edX (this will take a minute)...")
    
    if subject_list is None:
        subjects = all_subjects
    else:
        subjects = subject_list

    for subject in subjects:
        for i in range(5):
            url_str = 'https://www.edx.org/course-list/allschools/' + subject + '/allcourses'
            if i >= 1:
                url_str = url_str + '?page=' + unicode(i)
            edx_web = BeautifulSoup(urllib2.urlopen(url_str).read())
            for child in edx_web.find_all('h2', attrs={'class': 'title course-title'}):
                course_info = child.parent
                try:
                    title_list.append(course_info.a.contents[0].rstrip('\n'))
                    desc_list.append(course_info.div.contents[0].rstrip('\n'))
                    sub_list.append(subject)
                except:
                    pass

            for inst_info in edx_web.find_all('ul', attrs={'class': 'clearfix'}):
                instructor = re.search('(?<=Instructors:</span>)(.*)(?=</li>)', unicode(inst_info))
                uni = re.search('(?<=<li><strong>)(.*)(?=</strong></li>)', unicode(inst_info))
                try:
                    int_list.append(instructor.group(0).rstrip('\n'))
                    uni_list.append(uni.group(0).rstrip('\n'))
                except:
                    pass


def add_to_django():
    edx_provider, created = Provider.objects.get_or_create(name='edX')
    for i in range(len(title_list)):
        try:
            print "Adding " + title_list[i] + " course: " + str(i)
        except:
            pass
        c, created = Course.objects.get_or_create(name=title_list[i], description=desc_list[i], instructor=int_list[i])
        c.provider = edx_provider
        c.source, created = Source.objects.get_or_create(name=uni_list[i])
        c.save()
        subject, created = Subject.objects.get_or_create(name=sub_list[i])
        c.subjects.add(subject)
        c.save()
    print("Done!")
    print(str(len(title_list)) + " courses added!")


if __name__ == '__main__':
    run()
