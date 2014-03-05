from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^subjects', views.json_subjects, name='api_subjects'),
                       url(r'^courses', views.json_courses, name='api_courses'),
                       url(r'^enrolled_courses', views.json_enrolled_courses, name='enrolled_courses'),
                       url(r'^liked_subjects', views.json_liked_subjects, name='liked_subjects'),
                       url(r'^like_subject', views.like_subject, name='like_subject')
                       )
