from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^subjects', views.json_subjects, name='api_subjects'),
                       url(r'^courses', views.json_courses, name='api_courses'),
                       url(r'^enrolled_courses', views.json_enrolled_courses, name='enrolled_courses'),
                       url(r'^enroll', views.add_course, name='enroll'),
                       url(r'^drop', views.drop_course, name='drop'),
                       url(r'^liked_subjects', views.json_liked_subjects, name='liked_subjects'),
                       url(r'^like_subject', views.like_subject, name='like_subject'),
                       url(r'^dislike_subject', views.dislike_subject, name='dislike_subject'),
                       url(r'^complete_course', views.complete_course, name='complete_course'),
                       url(r'^sample_courses', views.sample_courses_for_subject, name='sample_courses')
                       )
