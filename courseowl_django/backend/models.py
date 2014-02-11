from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)
    provider = models.ForeignKey(Provider)
    description = models.CharField(max_length=3000)
    similarCourses = models.ManyToManyField('self')

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=100)
