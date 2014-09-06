# custom middleware classes
import timeseries.helpers as h
import re

__theme_regexes = {
	re.compile('^/(learn/?)?$') : "home",
	re.compile('^/(timeseries|data)/analyze') : "analyze",
	re.compile('^/projects') : "projects",
	re.compile('^/learn/greenhouse') : "greenhouse",
	re.compile('^/learn/solarwater') : "solarwater",
	re.compile('^/learn/weather') : "weather",
	re.compile('^/learn/solar') : "solar",
	re.compile('^/learn/geothermal') : "geothermal",
	re.compile('^/learn/electric') : "electric",
	re.compile('^/learn/hvac') : "hvac"
}

def systems_schema(request):
	"""this function populates all request contexts with the 'systems' variable"""
	return {"systems" : h.systems_schema()}

def theme(request):
	"""This Middleware class sets the "theme" variable in the template context to one of the following:
		[home, projects, analyze, greenhouse, solarwater, weather, solar, geothermal, electric, hvac]"""
	for regex, thm in __theme_regexes.iteritems():
		if regex.search(request.path) is not None:
			return {"theme" : thm}
	return {"theme" : "home"} # default case... render with home page theme