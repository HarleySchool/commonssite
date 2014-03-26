from django.conf.urls import patterns, url

from timeseries import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^request/', views.request_data, name='request data'),
	url(r'^chart/', views.chart, name='chart'),
	url(r'^vrf/', views.vrf_csv, name='vrf data'),
	url(r'^erv/', views.erv_csv, name='erv data'),
	url(r'^circuits/', views.channel_csv, name='electric circuits data'),
	url(r'^elec-summary/', views.elec_summary_csv, name='electric summary data'),
	url(r'^sma-panel/', views.solar_power_csv, name='solar power data'),
	url(r'^sma-weather/', views.solar_weather_csv, name='solar weather data'),
	url(r'^sma-over/', views.solar_overview_csv, name='solar overviews')
)