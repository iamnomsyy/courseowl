from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=1000)
    subjects = models.ManyToManyField(Subject)
    provider = models.ForeignKey(Provider, null=True, blank=True)
    description = models.CharField(max_length=3000)
    similarCourses = models.ManyToManyField('self')
    instructor = models.CharField(max_length=1000, null=True, blank=True)
    source = models.ForeignKey(Source, null=True, blank=True)

    def __unicode__(self):
        return self.name
