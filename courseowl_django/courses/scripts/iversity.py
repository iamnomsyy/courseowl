from courses.models import Provider, Course, Subject
import urllib2
from bs4 import BeautifulSoup


def run():
    print("Adding courses from iversity (this will take a minute)...")
    scrape()


def scrape():
    provider, created = Provider.objects.get_or_create(name='iversity')
    iversity_web = BeautifulSoup(urllib2.urlopen('https://iversity.org/courses').read())
    course_divs = iversity_web.find_all('article', class_='courses-list-item')

    for item in course_divs:
        create_course(item, provider)


def create_course(item, provider):
    subject = item.find('div', class_='ribbon-content').text.strip('\n')
    course_info = item.find('div', class_='course-body')
    title = course_info.a.text
    instructor_description_paragraphs = item.find_all('p')
    instructor = instructor_description_paragraphs[0].text.strip('\n')
    description = instructor_description_paragraphs[1].text.strip('\n')
    url = item.a.attrs['href']

    # print('Adding course:')
    # print('Subject: ' + subject)
    # print('Title: ' + title)
    # print('Instructor: ' + instructor)
    # print('Description: ' + description)
    # print('URL: ' + url)
    # print('===========================================')

    course, created = Course.objects.get_or_create(name=title, url=url, description=description, instructor=instructor, provider=provider)
    subject, created = Subject.objects.get_or_create(name=subject)
    course.subjects.add(subject)
    course.save()
