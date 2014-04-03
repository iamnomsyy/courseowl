from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^login', views.login, name='login'),
                       url(r'^signup', views.email_signup, name='email_signup'),
                       url(r'^logout', views.logout, name='logout'),
                       url(r'^deactivate_account', views.deactivate_account, name='deactivate_account'),
                       url(r'^profile', views.profile, name='profile')
                       )
