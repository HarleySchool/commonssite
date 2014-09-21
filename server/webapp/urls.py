from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	url(r'^/?$', TemplateView.as_view(template_name="main.html")),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^learn/', include('learn.urls')),
	url(r'^(timeseries|data)/', include('timeseries.urls')),
	url(r'^status/', 'timeseries.views.status')
)
