from courses.models import Subject, Provider, Course, Source
from accounts.models import UserProfile
from collections import defaultdict

# ######
# P U B L I C   I N T E R F A C E S
# ######


def get_all_subject_recommendations(user):
    """
    Entry point to get all subject-based recommendations
    """
    all_user_subjects = set()
    all_user_subjects.update(get_interest_subjects(user))
    all_user_subjects.update(get_enrolled_subjects(user))
    return get_recs_from_subjects(all_user_subjects)


def get_all_user_recommendations(user):
    '''
    Entry point to get all user-based recommendations
    '''
    best_user = get_most_similar_user(user)
    recommended_list = set()
    if not best_user:
        return recommended_list
    recommended_list.update(set(best_user.enrolled.all()))
    recommended_list.update(set(best_user.completed.all()))

    #Might as well get interest recommendation from this guy
    recommended_list.update(get_recs_from_subjects(set(best_user.interests.all())))

    return recommended_list


# ######
# H E L P E R   F U N C T I O N S
# ######


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
    Retrieves all courses in fuzzy subject matching set
    """
    subject_course_recs = set()
    for subject in subjects:
        for related_sub in get_fuzzy_subject_matching(subject):
            for course in Course.objects.filter(subjects=subject):
                print "Appending: " + course.name
                subject_course_recs.add(course)
    return subject_course_recs


def get_fuzzy_subject_matching(subject):
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
    for course in prefs.enrolled.all():
        subject_set.extend(course.subjects.all())
    for course in prefs.completed.all():
        subject_set.extend(course.subjects.all())
    return subject_set


def get_similar_user_interests(user):
    """
    Returns the most similar user to you based on shared interests
    """
    max_similar = 0
    most_similar_user = None

    prefs = UserProfile.objects.get(user=user)
    my_interests = set(prefs.interests.all())
    for other_user in UserProfile.objects.all():
        if other_user == prefs:
            continue
        similar_subs = my_interests.intersection(set(other_user.interests.all()))
        if len(similar_subs) > max_similar:
            max_similar = len(similar_subs)
            most_similar_user = other_user
    return most_similar_user, max_similar


def get_similar_user_dislikes(user):
    """
    Returns the most similar user to you based on shared dislikes
    """
    max_similar = 0
    most_similar_user = None

    prefs = UserProfile.objects.get(user=user)
    my_dislikes = set(prefs.disliked.all())
    for other_user in UserProfile.objects.all():
        if other_user == prefs:
            continue
        similar_dislikes = my_dislikes.intersection(set(other_user.disliked.all()))
        if len(similar_dislikes) > max_similar:
            max_similar = len(similar_dislikes)
            most_similar_user = other_user
    return most_similar_user, max_similar


def get_similar_user_enrolled(user):
    """
    Returns the most similar user to you based on shared enrolled
    """
    max_similar = 0
    most_similar_user = None

    prefs = UserProfile.objects.get(user=user)
    my_dislikes = set(prefs.enrolled.all())
    for other_user in UserProfile.objects.all():
        if other_user == prefs:
            continue
        similar_dislikes = my_dislikes.intersection(set(other_user.enrolled.all()))
        if len(similar_dislikes) > max_similar:
            max_similar = len(similar_dislikes)
            most_similar_user = other_user
    return most_similar_user, max_similar


def get_similar_user_completed(user):
    """
    Returns the most similar user to you based on shared completed
    """
    max_similar = 0
    most_similar_user = None

    prefs = UserProfile.objects.get(user=user)
    my_dislikes = set(prefs.completed.all())
    for other_user in UserProfile.objects.all():
        if other_user == prefs:
            continue
        similar_dislikes = my_dislikes.intersection(set(other_user.completed.all()))
        if len(similar_dislikes) > max_similar:
            max_similar = len(similar_dislikes)
            most_similar_user = other_user
    return most_similar_user, max_similar


def get_most_similar_user(user):
    """
    Computes scores and returns the user most similar to you
    """
    user_scores = defaultdict(int)
    similar_user, score = get_similar_user_interests(user)
    user_scores[similar_user] += score
    similar_user, score = get_similar_user_dislikes(user)
    user_scores[similar_user] += score
    similar_user, score = get_similar_user_enrolled(user)
    user_scores[similar_user] += score
    similar_user, score = get_similar_user_completed(user)
    user_scores[similar_user] += score
    max_score = 0
    best_user = None
    for similar_user, score in user_scores.items():
        if score > max_score:
            best_user = similar_user
            max_score = score
    return best_user
