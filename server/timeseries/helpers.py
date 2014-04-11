from timeseries.models import ModelRegistry
import dateutil.parser
from dateutil.tz import tzlocal

def systems_dict():
	"""construct and return a json object describing the different systems with available timeseries data. Note that no actual data is returned.
	A 'system' is something like 'HVAC' or 'Electric', and a subsystem is, for example, VRF within HVAC

	structure is as follows:
	{
		'system name' : {
			'subsystem name' : {
				id : 'CamelCaseId',
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
	# refer to https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types
	model_types = {
		'numeric' : [u'FloatField', u'IntegerField', u'BigIntegerField', u'DecimalField', u'PositiveIntegerField', u'PositiveSmallIntegerField', u'SmallIntegerField' ],
		'string' : [u'CharField', u'BooleanField', u'TextField']
	}
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
			'id' : registry.make_id(),
			'units' : {} # TODO
		}
	return systems

model_cache = {}
def get_registered_model(class_path):
	"""given the import path for a model (e.g. ModelRegistry.model_class), return the model class"""
	if class_path in model_cache:
		return model_cache[class_path]
	else:
		# import it
		path_parts = class_path.split('.')
		module_path = '.'.join(path_parts[:-1])
		class_name = path_parts[-1]
		mod = __import__(module_path, globals(), locals(), [class_name])
		model_cache[class_path] = getattr(mod, class_name)
		return model_cache[class_path]

scraper_cache = {}
def get_registered_scraper(scraper_path):
	"""given the import path for a scraper (e.g. ModelRegistry.scraper_class), return the scraper class"""
	if scraper_path in scraper_cache:
		return scraper_cache[scraper_path]
	else:
		# import it
		path_parts = scraper_path.split('.')
		module_path = '.'.join(path_parts[:-1])
		class_name = path_parts[-1]
		mod = __import__(module_path, globals(), locals(), [class_name])
		scraper_cache[scraper_path] = getattr(mod, class_name)
		return scraper_cache[scraper_path]

def parse_time(isostring):
	"""Parse an ISO datetime string into a datetime object. If no timezone information is given it's assumed to be local"""
	dt = dateutil.parser.parse(isostring)
	if dt.tzinfo == None: # if it's a naive datetime
		dt = dt.replace(tzinfo=tzlocal())
	return dt
