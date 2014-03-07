from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^subjects', views.json_subjects, name='api_subjects'),
                       url(r'^courses', views.json_courses, name='api_courses'),
                       url(r'^enrolled_courses', views.json_enrolled_courses, name='enrolled_courses'),
                       url(r'^enroll', views.add_course, name='enroll'),
                       url(r'^drop', views.drop_course, name='drop'),
                       )
