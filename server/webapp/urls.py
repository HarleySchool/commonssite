from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
admin.autodiscover()

class IndexView(TemplateView):
	template_name = "Main.html"

urlpatterns = patterns('',
	# Examples:
	url(r'^$', IndexView.as_view()),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^electric/', include('electric.urls')),
	#url(r'^hvac/', include('hvac.urls')),
	url(r'^(timeseries|data)/', include('timeseries.urls')),
	url(r'^status/', 'timeseries.views.status')
)
