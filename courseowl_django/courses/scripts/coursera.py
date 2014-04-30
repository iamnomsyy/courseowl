from courses.models import Course, Provider, Subject, Source
import json
import urllib2

from courses.scripts.utilities import unify_subject_name

def run():
    """
    Main function of the script. Gets JSON, parses, and adds the information to database
    """
    print('Adding Cousera courses....')
    coursera_json_url = 'https://www.coursera.org/maestro/api/topic/list?full=1%20or%20https://www.coursera.org/maestro/api/topic/list2'
    coursera_dict = get_and_parse_json(coursera_json_url)
    add_courses(coursera_dict)
    print("Done!")


def get_and_parse_json(url):
    """
    Gets JSON of all courses from provider and returns it as a dictionary
    """
    coursera_json_list = urllib2.urlopen(url)
    coursera_json_dict = json.loads(coursera_json_list.read())
    return coursera_json_dict


def add_courses(json_dict):
    """
    Adds courses from JSON into the database
    """
    coursera_provider, created = Provider.objects.get_or_create(name='Coursera')

    for course in json_dict:
        url = 'https://www.coursera.org/course/' + course['short_name']
        c, created = Course.objects.get_or_create(name=course['name'], description=course['short_description'], instructor=course['instructor'], url=url)
        c.provider = coursera_provider
        c.source, created = Source.objects.get_or_create(name=course['universities'][0]['name'])
        c.save()
        for category_id in course['category-ids']:
            better_subject_name = unify_subject_name(category_id)
            subject, created = Subject.objects.get_or_create(name=better_subject_name)
            c.subjects.add(subject)
        c.save()


if __name__ == '__main__':
    run()
