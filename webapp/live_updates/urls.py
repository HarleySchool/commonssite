from django.conf.urls import patterns, url

from live_updates import views

urlpatterns = patterns('',
	url(r'^$', views.initial, name='veris-tables-init'),
	url(r'^config/', views.config, name='config'),
	url(r'^update/', views.update, name='update')
)