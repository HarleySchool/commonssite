import json
from timeseries.models import Series
import timeseries.helpers as h
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

# step 1 of api communication: get information about what systems are available
def systems(request):
	# construct response
	return HttpResponse(content_type='application/json', content=json.dumps(h.systems_schema()))

# TODO use CSRF properly
@csrf_exempt
def save_series(request):
	post = json.loads(request.body)
	# TODO validate series
	# save it
	s = Series.lookup_or_save_series(post)
	response_dict = {
		'series_id' : s.string_hash
	}
	return HttpResponse(content_type='application/json', content=json.dumps(response_dict))

@csrf_exempt
def load_series(request):
	post = json.loads(request.body)
	try:
		s = Series.objects.get(string_hash=post.get("series_id"))
		return HttpResponse(content_type='application/json', content=json.dumps(s.spec))
	except:
		return HttpResponseNotFound()

@csrf_exempt
def series(request):
	"""construct and resturn a json object containing arrays of data corresponding to the requested fields.
	
	The REQUEST structure is a dict with at least three fields: 'from', 'to', and 'series', where 'series' is the filter_objs as defined by helpers.series_filter.
		further optional fields are 'temporary' and 'averages' which are booleans controlling whether temporary and/or average data are included in the response.
		default is averages=true and temporary=false.

	The RESPONSE structure is as specified in timeseries.helpers.series_filter (or see example below)
	
	REAL EXAMPLE: REQUEST
	{
		from : '2014-04-01T00:00:00-0400',
		to : '2014-04-02T00:00:00-0400',
		series : [{
			'system' : Electric',
			'subsystem' : 'Circuits',
			'indexes' : [1, 45],
			'columns' : ['Power', 'Current']
		},{
			'system' : 'Electric',
			'subsystem' : 'Overview',
			'indexes' : [],
			'columns' : ['TotalPower']
		}]
	}
	REAL EXAMPLE: RESPONSE
	[{
		'system' : 'Electric',
		'subsystem' : 'Circuits',
		'index' : 1,
		'data' : [	{'Time' : '2014-04-01T00:01:20-0400', 'Power' : 40.4, 'Current' : 8.2},
					{'Time' : '2014-04-01T00:01:53-0400', 'Power' : 36.5, 'Current' : 7.9},
					{'Time' : '2014-04-01T00:02:18-0400', 'Power' : 38.4, 'Current' : 8.1},
					...]
	},{
		'system' : 'Electric',
		'subsystem' : 'Circuits',
		'index' : 45,
		'data' : [	{'Time' : '2014-04-01T00:01:22', 'Power' : 12.8, 'Current' : 2.6},
					{'Time' : '2014-04-01T00:01:55', 'Power' : 15.0, 'Current' : 3.2},
					{'Time' : '2014-04-01T00:02:20', 'Power' : 14.9, 'Current' : 3.1},
					...]
	},{
		'system' : 'Electric',
		'subsystem' : 'Overview',
		'index' : null,
		'data' : [	{'Time' : '2014-04-01T00:01:24', 'TotalPower' : 13.9},
					{'Time' : '2014-04-01T00:01:57', 'TotalPower' : 14.3},
					{'Time' : '2014-04-01T00:02:22', 'TotalPower' : 11.6},
					...]
	}]
	"""
	if request.body:
		post = json.loads(request.body)
		t_start = h.parse_time(post.get('from'))
		t_end = h.parse_time(post.get('to'))
		temp = post.get('temporary', False)
		avg = post.get('averages', True)
		if t_start is None or t_end is None:
			return HttpResponseBadRequest("series request error: 'from' and 'to' range are required and must be specified as an ISO-formatted string")
		data = h.series_filter(post.get('series'), t_start, t_end, include_temporary=temp, include_averages=avg, isoformat=True)
		return HttpResponse(content_type='application/json', content=json.dumps(data))
	else:
		return HttpResponseBadRequest()

@csrf_exempt
def single(request):
	"""Get the latest data point(s) for the specified series. Definition of a series is identical to in the series() function above.
	"""
	if request.body:
		post = json.loads(request.body)
		data = h.live_filter(post.get('series'), isoformat=True)
		return HttpResponse(content_type='application/json', content=json.dumps(data))
	else:
		return HttpResponseBadRequest()
