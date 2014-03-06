from django.conf.urls import patterns, url

from live_updates import views

urlpatterns = patterns('',
	url(r'^$', views.initial, name='veris-tables-init'),
	url(r'^update/', views.refresh, name='update')
)