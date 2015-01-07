from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$',          TemplateView.as_view(template_name="learn/overview.html")),
	url(r'^electric/?$',   TemplateView.as_view(template_name="learn/electric.html")),
	url(r'^solar/?$',      TemplateView.as_view(template_name="learn/solar.html")),
	url(r'^greenhouse/?$', TemplateView.as_view(template_name="learn/greenhouse.html")),
	url(r'^hvac/?$',       TemplateView.as_view(template_name="learn/hvac.html")),
	url(r'^geothermal/?$', TemplateView.as_view(template_name="learn/geothermal.html")),
	url(r'^solarwater/?$', TemplateView.as_view(template_name="learn/solarwater.html")),
	url(r'^weather/?$',    TemplateView.as_view(template_name="learn/weather.html")),
	url(r'^software/?$',   TemplateView.as_view(template_name="learn/software.html")),
)