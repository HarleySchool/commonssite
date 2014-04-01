from django.http import HttpResponse
from timeseries.models import ModelRegistry
from commonssite.settings import datetime_out_format
import csv
import datetime
import pytz

# refer to https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types
model_types = {
	'numeric' : ['FloatField', 'IntegerField', 'BigIntegerField', 'DecimalField', 'PositiveIntegerField', 'PositiveSmallIntegerField', 'SmallIntegerField' ],
	'string' : ['CharField', 'BooleanField', 'TextField']
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
	for table in ModelRegistry.objects:
		if table.system not in systems:
			systems[table.system] = {}
		systems[table.system][table.short_name] = {
			'description' : table.description,
			'numbers' : []
		}
	return systems