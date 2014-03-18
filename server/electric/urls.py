from django.conf.urls import patterns, url

from electric import views

urlpatterns = patterns('',
	url(r'^$', views.diff_init, name='veris-tables-init'),
	url(r'^update/', views.diff_refresh, name='update'),
	url(r'^names/', views.name_map, name='channel names'),
	url(r'^update-names/', views.update_names, name='update channel names')
)
