from django.conf.urls import patterns, url

from live_updates import views

urlpatterns = patterns('',
	url(r'^$', views.updates, name='updates')
)