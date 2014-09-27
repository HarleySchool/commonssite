from django.conf.urls import patterns, url

from projects.views import search_project, view_project

urlpatterns = patterns('',
	url(r'^/?$', search_project),
	url(r'^(?P<slug>[\w\d\-]+)/?', view_project),
)
