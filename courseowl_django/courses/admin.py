from django.contrib import admin
from courses.models import Subject, Provider, Source, Course


class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Subject)
admin.site.register(Provider)
admin.site.register(Source)
admin.site.register(Course, CourseAdmin)
