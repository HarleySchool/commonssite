from django.conf.urls import patterns, url

from timeseries import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^vrf/', views.vrf_csv, name='vrf data'),
	url(r'^erv/', views.erv_csv, name='erv data'),
	url(r'^electric/', views.channel_csv, name='electric channel data')
)