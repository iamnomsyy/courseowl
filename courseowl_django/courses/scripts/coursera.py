from courses.models import Course, Provider, Subject, Source
import json
import urllib2


def run():
    print('Adding Cousera courses....')
    coursera_json_url = 'https://www.coursera.org/maestro/api/topic/list?full=1%20or%20https://www.coursera.org/maestro/api/topic/list2'
    coursera_dict = get_and_parse_json(coursera_json_url)
    add_courses(coursera_dict)
    print("Done!")


def get_and_parse_json(url):
    coursera_json_list = urllib2.urlopen(url)
    coursera_json_dict = json.loads(coursera_json_list.read())
    return coursera_json_dict


def add_courses(json_dict):
    coursera_provider, created = Provider.objects.get_or_create(name='Coursera')

    for course in json_dict:
        url = 'https://www.coursera.org/course/' + course['short_name']
        c, created = Course.objects.get_or_create(name=course['name'], description=course['short_description'], instructor=course['instructor'], url=url)
        c.provider = coursera_provider
        c.source, created = Source.objects.get_or_create(name=course['universities'][0]['name'])
        c.save()
        for category_id in course['category-ids']:
            subject, created = Subject.objects.get_or_create(name=category_id)
            c.subjects.add(subject)
        c.save()


if __name__ == '__main__':
    run()
