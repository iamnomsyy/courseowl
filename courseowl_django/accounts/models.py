from django.db import models
from django.contrib.auth.models import User
from courses.models import *


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, default='M')
    interests = models.ManyToManyField('courses.Subject', blank=True)
    providers = models.ManyToManyField('courses.Provider', blank=True)
    enrolled = models.ManyToManyField('courses.Course', blank=True)