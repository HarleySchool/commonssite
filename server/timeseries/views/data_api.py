import json
import datetime
import pytz
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

_epoch = datetime.datetime(1970,1,1)
_epoch = pytz.UTC.localize(_epoch)

# step 1 of api communication: get information about what systems are available
def get_systems(request):
	"""construct and return a json object describing the different systems with available timeseries data. Note that no actual data is returned.
	A 'system' is something like 'HVAC' or 'Electric', and a subsystem is, for example, VRF within HVAC

	structure is as follows:
	{
		'system name' : {
			'subsystem name' : {
				id : 'CamelCaseId',
				description : 'this is a really fancy and efficient subsystem',
				numeric : ['ColumnName1', 'ColumnName2'],
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
		systems[registry.system][registry.short_name] = {
			'description' : registry.description,
			'numeric' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['numeric']],
			'string' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['string']],
			'id' : registry.make_id(),
			'units' : {} # TODO
		}
	# construct response
	return HttpResponse(content_type='application/json', content=json.dumps(systems))

def query(request):
	"""construct and resturn a json object containing arrays of data corresponding to the requested fields
	
	REQUEST structure is as follows:
	{
		'system name:subsystem name' : {
			from : epoch-time-start,
			to : epoch-time-end,
			columns : ['ColumnName1', 'ColumnName2']
		}, ...
	}

	{
		'HVAC:VRF' : {
			from : Date.UTC(2014, 4, 1),
			to : Date.UTC(2014, 4, 8),
			columns : ['SetTemp', 'InletTemp']
		}
	}

	RESPONSE structure is as follows:
	{
		'system name:subsystem name' : {
			Time : [time0, time1, ..., timeN],
			SetTemp : [val0, val1, ..., valN],
			InletTemp : [val0, val1, ..., valN]
		}, ...
	}
	"""
	if request.method == 'GET':
		return render(request, "timeseries/chart.html", {})
	elif request.method == 'POST' and request.is_ajax():
		post = json.loads(request.body)
		data = {}
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
			# prepare data dict result
			data[full_name] = {}
			for c in cols:
				data[full_name][c] = []
			# perform the query on the database
			objects = model.objects.filter(Time__gte=t_start, Time__lt=t_end).values(*cols)
			# fun fact: values() causes the return value to be a dict rather than a Model object
			for obj in objects:
				for col, val in obj.iteritems():
					if col == 'Time':
						# a silly way to convert from a DateTime object into epoch time
						val = (val - _epoch).total_seconds()
					data[full_name][col].append(val)
		return HttpResponse(content_type='application/json', content=json.dumps(data))
	else:
		return HttpResponseBadRequest()