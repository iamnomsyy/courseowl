from django.db import models


class Subject(models.Model):
    """
    Subject, i.e. Economics.
    """
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Provider(models.Model):
    """
    The MOOC website provider, i.e. Coursera, edX.
    """
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Source(models.Model):
    """
    The university/creator of the course, i.e. UIUC, which can put courses on Coursera.
    """
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    """
    Course model, i.e. Pottery II.
    """
    name = models.CharField(max_length=1000)
    subjects = models.ManyToManyField(Subject)
    provider = models.ForeignKey(Provider, null=True, blank=True)
    description = models.CharField(max_length=3000)
    similarCourses = models.ManyToManyField('self')
    instructor = models.CharField(max_length=1000, null=True, blank=True)
    source = models.ForeignKey(Source, null=True, blank=True)

    def __unicode__(self):
        return self.name
