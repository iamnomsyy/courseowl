from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^login', views.login, name='login'),
                       url(r'^signup', views.email_signup, name='email_signup'),
                       url(r'^logout', views.logout, name='logout'),
                       url(r'^enroll', views.add_course, name='enroll'),
                       url(r'^drop', views.drop_course, name='drop')
                       )
