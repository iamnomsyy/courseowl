import courses.models
import accounts.models

'''
Gets recommendations based on what subjects the user is interested in.
'''
def get_subject_recommendations(user):
    # We should get other courses in the subjects of courses you are enrolled in
    subject_recs = set()
    my_subjects = list()
    prefs = UserProfile.objects.get(user=user)
    my_subjects.
    return subject_recs



def get_recs_from_subject(subjects):
    subject_course_recs = set()
    for subject in subjects:
        for related_sub in get_fuzzy_subject_maching(subject):
            for course in Course.objects.filter(subjects__icontains=subject, allowed=True):
                print "Appending: " + course.name
                subject_course_recs.add(course)
    return subject_course_recs



'''
Removes dashes in subject name and searches for related subjects
'''
def get_fuzzy_subject_maching(subject):
    sub_set = set()
    base_sub = str(subject.name).split('-')[0]
    related_subs = Subject.objects.filter(name__icontains=base_sub)
    for subject in related_subs:
        sub_set.add(subject)
    return sub_set

'''
Gets recommendations based off of the subjects of the classes you are enrolled in and completed.
'''
def get_enrolled_subject_recs(user):
    prefs = UserProfile.objects.get(user=user)
    subject_set = set()
    for course in prefs.enrolled:
        subject_set.update(course.subjects.all())
    for course in prefs.completed:
        subject_set.update(course.subjects.all())
