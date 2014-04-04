__author__ = 'David'

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



intList = list()
uniList = list()
titleList = list()
descList = list()
subList = list()


def run():
    populate_lists()
    add_to_django()


def populate_lists(subject_list=None):
    print "Adding courses from edx (this will take a minute)..."
    
    if subject_list == None:
        subjects = all_subjects
    else:
        subjects = subject_list

    for subject in subjects:
        for i in range(5):
            urlStr = 'https://www.edx.org/course-list/allschools/' + subject + '/allcourses'
            if i >= 1:
                urlStr = urlStr + '?page=' + unicode(i)
            edxWeb = BeautifulSoup(urllib2.urlopen(urlStr).read())
            for child in edxWeb.find_all('h2', attrs={'class' : 'title course-title'}):
                courseInfo = child.parent
                try:
                    titleList.append(courseInfo.a.contents[0].rstrip('\n'))
                    descList.append(courseInfo.div.contents[0].rstrip('\n'))
                    subList.append(subject)
                except:
                    pass

            for instInfo in edxWeb.find_all('ul', attrs={'class' : 'clearfix'}):
                instructor = re.search('(?<=Instructors:</span>)(.*)(?=</li>)', unicode(instInfo))
                uni = re.search('(?<=<li><strong>)(.*)(?=</strong></li>)', unicode(instInfo))
                try:
                    intList.append(instructor.group(0).rstrip('\n'))
                    uniList.append(uni.group(0).rstrip('\n'))
                except:
                    pass


def add_to_django():
    edxProvider, created = Provider.objects.get_or_create(name='edX')
    for i in range(len(titleList)):
        try:
            print "Adding " + titleList[i] + " course: " + str(i)
        except:
            pass
        c, created = Course.objects.get_or_create(name=titleList[i], description=descList[i], instructor=intList[i])
        c.provider = edxProvider
        c.source, created = Source.objects.get_or_create(name=uniList[i])
        c.save()
        subject, created = Subject.objects.get_or_create(name=subList[i])
        c.subjects.add(subject)
        c.save()
    print "Done!"
    print str(len(titleList)) + " courses added!"







if __name__ == '__main__':
    run()