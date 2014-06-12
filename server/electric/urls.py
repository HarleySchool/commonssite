from django.conf.urls import patterns, url

from electric import views

urlpatterns = patterns('',
	url(r'^$', views.diff_init, name='veris-tables-init'),
	url(r'^update/', views.diff_refresh, name='update')
)