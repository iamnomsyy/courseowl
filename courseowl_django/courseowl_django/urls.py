from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

import website.views

handler404 = 'website.views.error404'
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^api/', include('api.urls')),
                       url(r'^social_accounts/', include('allauth.urls')),
                       url(r'^search/', include('haystack.urls')),
                       url(r'^404/$', website.views.error404),
                       url(r'^', include('website.urls')),
                       )
