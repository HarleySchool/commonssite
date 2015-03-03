from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.conf.urls.static import static
import settings
admin.autodiscover()

handler500 = 'timeseries.views.error500'

urlpatterns = patterns('',
	# Examples:
	url(r'^/?$', TemplateView.as_view(template_name="main.html")),
	url(r'^projects/', include('projects.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^learn/', include('learn.urls')),
	url(r'^(timeseries|data)/', include('timeseries.urls')),
	url(r'^status/', 'timeseries.views.status')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # serve media files (DEVELOPMENT ENVIRONMENT ONLY)
