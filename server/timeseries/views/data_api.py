import json
import timeseries.helpers as h
from django.views.decorators.csrf import csrf_exempt
from timeseries.models import ModelRegistry
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

# step 1 of api communication: get information about what systems are available
def systems(request):
	# construct response
	return HttpResponse(content_type='application/json', content=json.dumps(h.systems_dict()))

@csrf_exempt
def series(request):
	"""construct and resturn a json object containing arrays of data corresponding to the requested fields
	
	REQUEST structure is as specified in timeseries.helpers.system_filter

	RESPONSE structure is as follows:
	{
		'series name' : {
			Time : [time0 (isostring), time1 (isostring), ..., timeN (isostring)],
			ColumnName1 : [val0, val1, ..., valN],
			ColumnName2 : [val0, val1, ..., valN]
		}, ...
	}
	
	REAL EXAMPLE: REQUEST
	{
		'electric:Electric Overview' : {
			from : '2014-04-01T00:00:00-0400',
			to : '2014-04-02T00:00:00-0400',
			series : ['Panel=Panel 2&Channel=Channel #17'],
			columns : ['TotalPower', 'MaxPower']
		}
	}
	REAL EXAMPLE: RESPONSE
	{
		'Panel 2: Channel #17' : {
			Time : ['2014-04-08T08:00:00-0400', '2014-04-08T08:20:00-0400', '2014-04-08T08:40:00-0400', ...]
			TotalPower : [10.4, 10.1, 8.0, ...],
			MaxPower : [11.0, 10.5, 8.2]
		}, ...
	}
	"""
	if request.method == 'POST' and request.is_ajax():
		post = json.loads(request.body)
		data = {}
		multi_system = len(post) > 1
		for full_name, spec in post.iteritems():
			sys_name = full_name.split(':')[0]
			sub_name = full_name.split(':')[1]
			# get requested model parameters from registry
			try:
				registry = ModelRegistry.objects.get(system=sys_name, short_name=sub_name)
			except ObjectDoesNotExist:
				print "bad query for system %s and subsystem %s" % (sys_name, sub_name)
				continue
			# using registry, get the actual model
			model = h.get_registered_model(registry.model_class)
			# prepare the query on the database
			t_start = h.parse_time(spec.get('from'))
			t_end = h.parse_time(spec.get('to'))
			cols = spec.get('columns')
			if 'Time' not in cols:
				cols.append('Time')
			if spec['series'] == []:
				spec['series'] = ['']
			for series in spec['series']:
				# parsing series is sort of tricky. Given a filter that doesn't uniquely identify
				# a series, we return _all_ matching series. (for example, 'Panel=Panel 2' will
				# return all 42 channels)
				# header_permutations will be a list of all unique {name:value, name2:value2} groups
				header_permutations = model.get_series_identifiers()
				# now we use the filter function to narrow down to just the selected headers
				filtered_headers = header_permutations
				if series != '':
					for series_filter in series.split('&'):
						filter_col_name = series_filter.split('=')[0]
						filter_val      = series_filter.split('=')[1]
						filtered_headers = filter(lambda d: d[filter_col_name] == filter_val, filtered_headers)
				print "HEADER FILTER"
				print filtered_headers
				for unique_header_permutation in filtered_headers:
					series_name = ': '.join(unique_header_permutation.values())
					if multi_system:
						series_name = sub_name + ': ' + series_name
					# prepare data dict result
					data[series_name] = {}
					for col in cols:
						data[series_name][col] = []
					# perform the query on the database
					#keys = unique_header_permutation.keys()
					# convert this:
					# {name: val, name2: val2}
					# into this:
					# {name__eq: val, name2__eq: val2}
					#header_kwarg_filter = dict([(k+"__eq", str(unique_header_permutation[k])) for k in keys])
					#print header_kwarg_filter
					# query the database on the given time interval and selecting for the given headers
					objects = model.objects.filter(Time__gte=t_start, Time__lt=t_end, **unique_header_permutation).values(*cols)
					# fun fact: values() causes the return value to be a dict rather than a Model object
					for obj in objects:
						for col, val in obj.iteritems():
							if col == 'Time':
								val = val.isoformat()
							data[series_name][col].append(val)
		return HttpResponse(content_type='application/json', content=json.dumps(data))
	else:
		return HttpResponseBadRequest()

@csrf_exempt
def single(request):
	"""using a scraper, return a single live data point"""
	pass