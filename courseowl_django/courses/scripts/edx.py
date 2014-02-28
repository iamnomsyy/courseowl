__author__ = 'David'

#from ..models import *
import urllib2
from bs4 import BeautifulSoup
import re

subjects = [
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


def run():
    for subject in subjects:
        for i in range(10):
            titleList = list()
            descList = list()
            urlStr = 'https://www.edx.org/course-list/allschools/' + subject + '/allcourses'
            if i >= 1:
                urlStr = urlStr + '?page=' + unicode(i)
            print urlStr
            edxWeb = BeautifulSoup(urllib2.urlopen(urlStr).read())
            for child in edxWeb.find_all('h2', attrs={'class' : 'title course-title'}):
                courseInfo = child.parent
                try:
                    print courseInfo.a.contents[0]
                    titleList.append(courseInfo.a.contents[0])
                    print courseInfo.div.contents[0]
                    descList.append(courseInfo.div.contents[0])
                    print '\n\n'
                except:
                    pass

            intList = list()
            uniList = list()
            for instInfo in edxWeb.find_all('ul', attrs={'class' : 'clearfix'}):
                instructor = re.search('(?<=Instructors:</span>)(.*)(?=</li>)', unicode(instInfo))
                uni = re.search('(?<=<li><strong>)(.*)(?=</strong></li>)', unicode(instInfo))
                try:
                    print instructor.group(0)
                    print uni.group(0)
                    intList.append(instructor.group(0))
                    uniList.append(uni.group(0))
                except:
                    pass
    for i in range(len(titleList)):
        print 'Title: ' + titleList[i]
        print 'Description: ' + descList[i]
        print 'Instructor: ' + intList[i]
        print 'University: ' + uniList[i] + '\n\n'







if __name__ == '__main__':
    run()