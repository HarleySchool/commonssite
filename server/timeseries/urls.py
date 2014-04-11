from django.conf.urls import patterns, url

from timeseries import views

urlpatterns = patterns('',
	url(r'^$', views.makedownload, name='index'),
	url(r'^live/', views.live, name='live graphs'),
	url(r'^makechart/', views.makechart, name='make chart'),
	url(r'^api/systems/', views.systems, name='get systems'),
	url(r'^api/series/', views.series, name='get series'),
	url(r'^api/single/', views.single, name='get single point'),
	url(r'^api/csv/', views.download_csv, name='download csv')
)