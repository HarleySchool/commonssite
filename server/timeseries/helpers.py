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

def series_filter(filter_obj, tstart, tend):
	"""
	Takes a definition of one or more series and returns a list of dicts with 'H' and 'D' fields for Headers and Data respectively.
	All headers (e.g. Time, Name) will always be returned.

	filter definition is as follows:
	{
		'system name' : {
			'subsystem name' : {
				series : {
					'header1' : ['value1', 'value2', ...],
					'header2' : ['valueX', 'valueY', ...]
				},
				columns : ['ColumnName1', 'ColumnName2']
			}, ...
		}, ...
	}

	Note that setting columns to '[]' is interpreted as all columns.
	"""
	retlist = []
	for sys, subs in filter_obj.iteritems():
		for subsys, specs in subs.iteritems():
			# look up the requested system in our registry
			m = ModelRegistry.objects.get(system=sys, short_name=subsys)
			# if it doesn't exist, skip this one
			if not m:
				continue
			# get the corresponding model class
			model = get_registered_model(m.model_class)
			filter_kwargs = {}
			# filter by header and value
			for h, vals in specs.get('series').iteritems():
				param = h + '__in' # django syntax for "all values in a list"
				filter_kwargs[param] = []
				for v in vals:
					filter_kwargs[param].append(v)
			# start the queryset as empty (will be built up by filters)
			Q = model.objects.filter(Time__gte=tstart, Time__lt=tend, **filter_kwargs)
			# filter for only the selected columns
			# note that if 'columns' is None or [], no filtering is performed and all columns are returned
			data_columns = specs.get('columns')
			all_columns = data_columns[:]
			if all_columns:
				for head in model.get_header_names():
					if head not in all_columns:
						all_columns.append(head)
			else:
				all_columns = model.get_header_names() + model.get_field_names()
			Q = Q.values(*all_columns)
			for obj in Q:
				hd_dict = {'H' : {}, 'D' : {}}
				for head in model.get_header_names():
					if head != 'Time':
						hd_dict['H'][head] = obj.__dict__[head]
				for point in data_columns:
					hd_dict['D'][point] = obj.__dict__[point]
				hd_dict['Time'] = obj.__dict__['Time']
				retlist.append(hd_dict)
	return retlist

def live_filter(filter_obj):
	"""see series_filter for api (identical)"""
	retlist = []
	for sys, subs in filter_obj.iteritems():
		for subsys, specs in subs.iteritems():
			# look up the requested system in our registry
			m = ModelRegistry.objects.get(system=sys, short_name=subsys)
			# if it doesn't exist, skip this one
			if not m:
				continue
			# get the corresponding model class
			model = get_registered_model(m.model_class)
			scraper_class = get_registered_scraper(m.scraper_class)
			scraper = scraper_class()
			# perform a scrape!
			new_data = scraper.get_data()
			# use the series filters
			for h, vals in specs.get('series').iteritems():
				new_data = filter(lambda obj: obj.__dict__.get(h) in vals, new_data)
			# filter for only the selected columns
			# note that if 'columns' is None or [], no filtering is performed and all columns are returned
			data_columns = specs.get('columns')
			all_columns = data_columns[:]
			if all_columns:
				for head in model.get_header_names():
					if head not in all_columns:
						all_columns.append(head)
			else:
				all_columns = model.get_header_names() + model.get_field_names()
			for obj in new_data:
				hd_dict = {'H' : {}, 'D' : {}}
				for head in model.get_header_names():
					if head != 'Time':
						hd_dict['H'][head] = obj.__dict__[head]
				for point in data_columns:
					hd_dict['D'][point] = obj.__dict__[point]
				hd_dict['Time'] = obj.__dict__['Time']
				retlist.append(hd_dict)
	return retlist