from django.conf.urls import patterns, url
import website.views

urlpatterns = patterns('',
                       url(r'^subject_preferences', website.views.subject_preferences, name='website_subject_preferences'),
                       url(r'^course_preferences', website.views.course_preferences, name='website_course_preferences'),
                       url(r'^$', website.views.index, name='website_index')
)
