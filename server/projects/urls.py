from django.conf.urls import patterns, url

from projects.views import list_recent, view_project

urlpatterns = patterns('',
	url(r'^$', list_recent),
	url(r'^(?P<slug>[\w\d\-]+)/?$', view_project),
)
