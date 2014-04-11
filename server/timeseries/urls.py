from django.conf.urls import patterns, url

from timeseries import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^api/systems/', views.get_systems, name='get systems'),
	url(r'^api/query/', views.query, name='get systems'),
	url(r'^download/(?P<model_name>.*)/', views.generic_csv, name='download csv')
)