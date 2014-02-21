from django.conf.urls import patterns, url
import website.views

urlpatterns = patterns('',
    url(r'^$', website.views.index, name='website_index')
)
