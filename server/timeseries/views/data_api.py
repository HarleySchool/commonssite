import json
import timeseries.helpers as h
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

# step 1 of api communication: get information about what systems are available
def systems(request):
	# construct response
	return HttpResponse(content_type='application/json', content=json.dumps(h.systems_dict()))

@csrf_exempt
def series(request):
	"""construct and resturn a json object containing arrays of data corresponding to the requested fields
	
	RESPONSE structure is as specified in timeseries.helpers.series_filter,
	The REQUEST structure is a dict with three fields: 'from', 'to', and 'series', where 'series' is the filter_list as defined by series_filter
	
	REAL EXAMPLE: REQUEST
	{
		from : '2014-04-01T00:00:00-0400',
		to : '2014-04-02T00:00:00-0400',
		series : [{
		'Electric' : {
			'Circuits' : {
				'series' : {
					'Channel' : ['Channel #1', 'Channel #4'],
					'Panel' : ['Panel 2']
				},
				'columns' : ['TotalPower', 'MaxPower']
			}
		}]
	}
	REAL EXAMPLE: RESPONSE
	[{
		'H' : {
			'Time' : 2014-04-01T00:02:32-0400,
			'Panel' : 'Panel 2',
			'Channel' : 'Channel #1'},
		'D' : {
			'TotalPower' : 0.823,
			'MaxPower' : 0.901
		}
	},
	{
		'H' : {
			'Time' : 2014-04-01T00:02:33-0400,
			'Panel' : 'Panel 2',
			'Channel' : 'Channel #2'},
		'D' : {
			'TotalPower' : 0.223,
			'MaxPower' : 0.301
		}
	},
	}, ... et cetera]
	"""
	if request.method == 'POST' and request.is_ajax():
		post = json.loads(request.body)
		t_start = h.parse_time(post.get('from'))
		t_end = h.parse_time(post.get('to'))
		temp = post.get('temporary', False)
		avg = post.get('averages', True)
		if t_start is None or t_end is None:
			return HttpResponseBadRequest("series request error: 'from' and 'to' range are required and must be specified as an ISO-formatted string")
		data = h.series_filter(post.get('series'), t_start, t_end, include_temporary=temp, include_averages=avg)
		# check for time formatting
		for obj in data:
			obj['Time'] = obj['Time'].isoformat()
		return HttpResponse(content_type='application/json', content=json.dumps(data))
	else:
		return HttpResponseBadRequest()

@csrf_exempt
def single(request):
	"""using a scraper, return a single live data point. API is identical to series() (but from: and to: are not needed)
	"""
	if request.method == 'POST' and request.is_ajax():
		post = json.loads(request.body)
		data = h.live_filter(post.get('series'))
		# check for time formatting
		for obj in data:
			obj['Time'] = obj['Time'].isoformat()
		return HttpResponse(content_type='application/json', content=json.dumps(data))
	else:
		return HttpResponseBadRequest()