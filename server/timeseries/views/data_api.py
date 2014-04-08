import json
import datetime
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from timeseries.models import ModelRegistry
from timeseries import get_registered_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

# refer to https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types
model_types = {
	'numeric' : [u'FloatField', u'IntegerField', u'BigIntegerField', u'DecimalField', u'PositiveIntegerField', u'PositiveSmallIntegerField', u'SmallIntegerField' ],
	'string' : [u'CharField', u'BooleanField', u'TextField']
}

# step 1 of api communication: get information about what systems are available
def get_systems(request):
	"""construct and return a json object describing the different systems with available timeseries data. Note that no actual data is returned.
	A 'system' is something like 'HVAC' or 'Electric', and a subsystem is, for example, VRF within HVAC

	structure is as follows:
	{
		'system name' : {
			'subsystem name' : {
				description : 'this is a really fancy and efficient subsystem',
				numeric : ['ColumnName1', 'ColumnName2'],
				selection : {
					'header1' : ['unique_value1', 'unique_value2'],
					...
				}
				units : {
					'ColumnName1' : 'in',
					'ColumnName2' : 'kWh'
				}
				string : ['ColumnNameA', 'ColumnNameB'],
			}, ...
		}, ...
	}
	"""
	systems = {}
	# start with the ModelRegistry - that's where we keep track of models and scrapers
	for registry in ModelRegistry.objects.all():
		if registry.system not in systems:
			systems[registry.system] = {}
		model = get_registered_model(registry.model_class)
		# construct 'selection' based on unique headers
		header_selections = {}
		all_headers = model.get_header_names()
		all_headers.remove('Time')
		for h in all_headers:
			header_selections[h] = [str(val) for val in model.objects.values_list(h, flat=True).distinct()]
		systems[registry.system][registry.short_name] = {
			'description' : registry.description,
			'numeric' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['numeric']],
			'string' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['string']],
			'selection' : header_selections,
			'units' : {} # TODO
		}
	# construct response
	return HttpResponse(content_type='application/json', content=json.dumps(systems))

# convert a datetime.timedelta object into total seconds
# (used in computing epoch time)
def __td_seconds(timedelta):
	return timedelta.seconds + timedelta.days*3600*24

_epoch = datetime.datetime(1970,1,1)
_epoch = pytz.UTC.localize(_epoch)
def __epoch(date):
	return __td_seconds(date - _epoch)

@csrf_exempt
def query(request):
	"""construct and resturn a json object containing arrays of data corresponding to the requested fields
	
	REQUEST structure is as follows:
	{
		'system name:subsystem name' : {
			from : epoch-time-start,
			to : epoch-time-end,
			series : ['header1=val1&header2=valx', 'header1=val2&header2=valx'], // [] is interpreted as 'all series'
			columns : ['ColumnName1', 'ColumnName2']
		}, ...
	}

	RESPONSE structure is as follows:
	{
		'series name' : {
			Time : [time0, time1, ..., timeN],
			ColumnName1 : [val0, val1, ..., valN],
			ColumnName2 : [val0, val1, ..., valN]
		}, ...
	}
	
	REAL EXAMPLE: REQUEST
	{
		'electric:Electric Overview' : {
			from : Date.UTC(2014, 4, 1),
			to : Date.UTC(2014, 4, 8),
			series : ['Panel=Panel 2&Channel=Channel #17'],
			columns : ['TotalPower', 'MaxPower']
		}
	}
	REAL EXAMPLE: RESPONSE
	{
		'Panel 2: Channel #17' : {
			Time : [1368921000, 1368993000, 1369075000, ...]
			TotalPower : [10.4, 10.1, 8.0, ...],
			MaxPower : [11.0, 10.5, 8.2]
		}
	}
	"""
	if request.method == 'GET':
		return render(request, "timeseries/chart.html", {})
	elif request.method == 'POST' and request.is_ajax():
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
			model = get_registered_model(registry.model_class)
			# prepare the query on the database
			t_start = datetime.datetime.utcfromtimestamp(spec.get('from'))
			t_start = pytz.UTC.localize(t_start)
			t_end = datetime.datetime.utcfromtimestamp(spec.get('to'))
			t_end = pytz.UTC.localize(t_end)
			cols = spec.get('columns')
			if 'Time' not in cols:
				cols.append('Time')
			for series in spec['series']:
				# parsing series is sort of tricky. Given a filter that doesn't uniquely identify
				# a series, we return _all_ matching series. (for example, 'Panel=Panel 2' will
				# return all 42 channels)
				# header_permutations will be a list of all unique {name:value, name2:value2} groups
				header_permutations = model.get_series_identifiers()
				# now we use the filter function to narrow down to just the selected headers
				filtered_headers = header_permutations
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
					for c in cols:
						data[series_name][c] = []
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
								val = __epoch(val)
							data[series_name][col].append(val)
		return HttpResponse(content_type='application/json', content=json.dumps(data))
	else:
		return HttpResponseBadRequest()
