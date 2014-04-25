from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    interests = models.ManyToManyField('courses.Subject', blank=True)
    providers = models.ManyToManyField('courses.Provider', blank=True)
    enrolled = models.ManyToManyField('courses.Course', blank=True, related_name='enrolled_classes')
    completed = models.ManyToManyField('courses.Course', blank=True, related_name='completed_classes')
    disliked = models.ManyToManyField('courses.Course', blank=True, related_name='disliked_classes')

    def __unicode__(self):
        return self.user.email
