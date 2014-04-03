import urllib2
import json
from bs4 import BeautifulSoup
from courses.models import *

def get_urls():
    url = "http://www.udacity.com/wiki/frontpage"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read()

    soup = BeautifulSoup(page)

    # a list of <li> elements that 
    list_courses = soup.body.div.find_all('div')[2].find_all('div')[4].ul.find_all('li')

    list_course_urls = []
    for course in list_courses:
        course_str = str(course).lower()
        list_course_urls.append('https://www.udacity.com/course/' + course_str[4:9])

    return list_course_urls

def get_page(url):
    # get the page
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read()

    # get the text on the page
    soup = BeautifulSoup(page)
    page_text = soup.get_text().encode('UTF-8')
    page_text = page_text.replace('\t', '')
    page_text = page_text.split('\n')

    page_text_list = []

    for item in page_text:
        if item != '':
            page_text_list.append(item)

    return page_text_list

def get_name(page):
    anchor = page.index('View Trailer')
    return page[anchor+1]

def get_instr(page):
    instr = []

    anchor_x = page.index('Instructors & Partners')
    anchor_y = page.index('Ways to Take This Course')

    for i in range(anchor_x, anchor_y):
        if page[i] == 'Instructor':
            instr.append(page[i-1])

    return ', '.join(instr)

def get_desc(page):
    anchor = page.index('Course Summary')
    return page[anchor+1]

def get_subj(page):
    subj = []

    try:
        anchor_x = page.index('This Course is a Part Of')
        anchor_y = page.index('Course Instructors')
        subj = page[anchor_x+1 : anchor_y]
    except ValueError:
        subj = []

    # remove the word 'Track'
    good_subj = []
    for item in subj:
        good_subj.append(item[:-6])

    return good_subj

def get_all_courses(urls=None):
    course_urls = urls
    if urls == None:
        course_urls = get_urls()
    all_courses = {}

    for url in course_urls:
        page = get_page(url)
        name = get_name(page) # string
        instr = get_instr(page) # list of strings
        desc  = get_desc(page)  # string
        subj  = get_subj(page)  # list of strings

        all_courses[name] = {'name': name, 'instr': instr, 'desc': desc, 'subj': subj}

        print("obtained data for course: " + name)

    return all_courses

def run():
    all_courses = get_all_courses()

    udacityProvider, created = Provider.objects.get_or_create(name='Udacity')

    for name, course in all_courses.iteritems():
        c, created = Course.objects.get_or_create(name=course['name'], description=course['desc'], instructor=course['instr'])
        c.provider = udacityProvider
        # source university not easily available in udacity
        # c.source, created = ....
        c.save()
        for categoryId in course['subj']:
            subject, created = Subject.objects.get_or_create(name=categoryId)
            c.subjects.add(subject)
        c.save()

if __name__ == '__main__':
    run()

