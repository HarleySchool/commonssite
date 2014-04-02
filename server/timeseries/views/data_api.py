import json
from django.http import HttpResponse
from timeseries.models import ModelRegistry
from timeseries import get_registered_model

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
	for table in ModelRegistry.objects.all():
		if table.system not in systems:
			systems[table.system] = {}
		model = get_registered_model(table.model_class)
		systems[table.system][table.short_name] = {
			'description' : table.description,
			'numeric' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['numeric']],
			'string' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['string']],
			'units' : {} # TODO
		}
	# construct response
	return HttpResponse(content_type='application/json', content=json.dumps(systems))
