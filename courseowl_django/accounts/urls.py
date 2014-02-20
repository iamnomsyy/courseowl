from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^login', views.login, name='login'),
                       # url(r'^google_login', views.google_login, name='google login')
                       )
