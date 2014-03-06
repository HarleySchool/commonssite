from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
admin.autodiscover()

class IndexView(TemplateView):
    template_name = "base.html"

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include('data.urls')),
    url(r'^verisupdate/', include('live_updates.urls'))
)
