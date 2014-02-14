from django.db import models
from django.contrib.auth.models import User
#from courses.models import *


''''class UserProfile(models.Model):
    username = models.OneToOneField(User)
    email = models.CharField(max_length=100, blank=True, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    gender = models.CharField(max_length=1, default='M')
    interests = models.ManyToManyField('courses.Subject')
    providers = models.ManyToManyField('courses.Provider')
    enrolled = models.ManyToManyField('courses.Course')
    completed = models.ManyToManyField('courses.Course')

    def __unicode__(self):
        return self.email'''