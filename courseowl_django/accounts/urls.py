from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^login', views.login, name='login'),
                       url(r'^signup', views.email_signup, name='email_signup'),
                       url(r'^logout', views.logout, name='logout'),
                       url(r'^delete_account', views.delete_account, name='delete+account'),
                       url(r'^profile', views.profile, name='profile'),
                       url(r'^change_password', views.change_password, name='change_password'),
                       )
