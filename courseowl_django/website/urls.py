from django.conf.urls import patterns, url
import website.views

urlpatterns = patterns('',
                       url(r'^personalize/', website.views.personalize, name='website_personalize'),
                       url(r'^$', website.views.index, name='website_index')
)
