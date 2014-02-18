from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^login', views.do_login, name='do_login')
)
