from django.contrib import admin
from .models import Subject, Provider, Source, Course

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
     search_fields = ['name']

admin.site.register(Subject)
admin.site.register(Provider)
admin.site.register(Source)
admin.site.register(Course, CourseAdmin)
