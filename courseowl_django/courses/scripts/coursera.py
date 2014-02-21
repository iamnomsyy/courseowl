from ..models import *
import json
import urllib2



def run():
    courseraJsonUrl = 'https://www.coursera.org/maestro/api/topic/list?full=1%20or%20https://www.coursera.org/maestro/api/topic/list2'
    courseraDict = getAndParseJson(courseraJsonUrl)
    addCourses(courseraDict)

def getAndParseJson(url):
    courseraJsonList = urllib2.urlopen(url)
    courseraJsonDict = json.loads(courseraJsonList.read())
    return courseraJsonDict

def addCourses(jsonDict):
    courseraProvider, created = Provider.objects.get_or_create(name='coursera')

    for course in jsonDict:
        c, created = Course.objects.get_or_create(name=course['name'], description=course['short_description'], instructor=course['instructor'])
        c.provider = courseraProvider
        c.source, created = Source.objects.get_or_create(name=course['universities'][0]['name'])
        c.save()
        for categoryId in course['category-ids']:
            subject, created = Subject.objects.get_or_create(name=categoryId)
            c.subjects.add(subject)
        c.save()



if __name__ == '__main__':
    run()
