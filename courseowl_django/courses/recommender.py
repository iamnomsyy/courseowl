import courses.models
import accounts.models


def get_interest_subjects(user):
    """
    Gets subjects based on what subjects the user is interested in.
    """
    # We should get other courses in the subjects of courses you are enrolled in
    my_subjects = list()
    prefs = UserProfile.objects.get(user=user)
    my_subjects.extend(prefs.interests.all())
    return my_subjects

def get_recs_from_subjects(subjects):
    """
    Retreives all coureses in fuzzy subject matching set
    """
    subject_course_recs = set()
    for subject in subjects:
        for related_sub in get_fuzzy_subject_maching(subject):
            for course in Course.objects.filter(subjects__icontains=subject, allowed=True):
                print "Appending: " + course.name
                subject_course_recs.add(course)
    return subject_course_recs



def get_fuzzy_subject_maching(subject):
    """
    Removes dashes in subject name and searches for related subjects
    """
    sub_set = set()
    base_sub = str(subject.name).split('-')[0]
    related_subs = Subject.objects.filter(name__icontains=base_sub)
    for subject in related_subs:
        sub_set.add(subject)
    return sub_set


def get_enrolled_subjects(user):
    """
    Gets subjects based off of the subjects of the classes you are enrolled in and completed.
    """
    prefs = UserProfile.objects.get(user=user)
    subject_set = list()
    for course in prefs.enrolled:
        subject_set.extend(course.subjects.all())
    for course in prefs.completed:
        subject_set.extend(course.subjects.all())
    return subject_set


def get_all_subject_recommendations(user):
    """
    Gets all subject-based course recommendations
    """
    all_user_subjects = set()
    all_user_subjects.update(get_interest_subjects(user))
    all_user_subjects.update(get_enrolled_subjects(user))
    return get_recs_from_subjects(all_user_subjects)

def get_similar_user_interests(user):
    """
    Returns the most similar user to you based on shared interests
    """
    max_similar = 0
    most_similar_user = None

    prefs = UserProfile.objects.get(user=user)
    my_interests = set(prefs.interests.all())
    for other_user in UserProfile.objects.all():
        similar_subs = my_interests.intersection(set(other_user.interests.all()))
        if len(similar_subs) > max_similar:
            max_similar = len(similar_subs)
            most_similar_user = other_user
    return most_similar_user

def get_similar_user_dislikes(user):
    """
    Returns the most similar user to you based on shared dislikes
    """
    max_similar = 0
    most_similar_user = None

    prefs = UserProfile.objects.get(user=user)
    my_dislikes = set(prefs.disliked.all())
    for other_user in UserProfile.objects.all():
        similar_dislikes = my_dislikes