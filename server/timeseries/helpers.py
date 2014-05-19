from timeseries.models import ModelRegistry
import dateutil.parser
from dateutil.tz import tzlocal

# refer to https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types
model_types = {
	'numeric' : [u'FloatField', u'IntegerField', u'BigIntegerField', u'DecimalField', u'PositiveIntegerField', u'PositiveSmallIntegerField', u'SmallIntegerField' ],
	'string' : [u'CharField', u'BooleanField', u'TextField']
}

def systems_dict():
	"""construct and return a json object describing the different systems with available timeseries data. Note that no actual data is returned.
	A 'system' is something like 'HVAC' or 'Electric', and a subsystem is, for example, VRF within HVAC

	structure is as follows:
	{
		'system name' : {
			'subsystem name' : {
				id : 'CamelCaseId',
				description : 'this is a really fancy and efficient subsystem',
				status : 0, // 0, 1, or 2. see timeseries.models.ModelRegistry for what they mean.
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
			header_selections[h] = [str(val) for val in model.objects.filter(Time=model.latest()).values_list(h, flat=True).distinct()]
		systems[registry.system][registry.short_name] = {
			'description' : registry.description,
			'status' : registry.status,
			'numeric' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['numeric']],
			'string' : [f.name for f in model._meta.fields if f.get_internal_type() in model_types['string']],
			'selection' : header_selections,
			'id' : registry.make_id(),
			'units' : {} # TODO
		}
	return systems

def split_on_indexes(queryset):
	"""given a queryset of TimeseriesBase objects, return a dict mapping from each unique index to the list of
	objects which share that index"""
	index_lookup = {}
	for obj in queryset:
		ind = obj.index() # index() method is defined in TimeseriesBase. it returns a tuple of index values
		index_lookup[ind] = index_lookup.get(ind, []) + [obj] # append the current object to this list
	return index_lookup

def timedelta_seconds(timedelta):
	"""get the total seconds in a timedelta object"""
	return timedelta.days * 86400 + timedelta.seconds

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

def __obj_list_to_hd_dict(obj_list, model, columns):
	retlist = []
	for obj in obj_list:
		hd_dict = {'H' : {}, 'D' : {}}
		for head in model.get_header_names():
			if head != 'Time':
				hd_dict['H'][head] = obj[head]
		for point in columns:
			hd_dict['D'][point] = obj[point]
		hd_dict['Time'] = obj['Time']
		retlist.append(hd_dict)
	retlist.sort(key=lambda d: d['Time'])
	return retlist

def series_filter(filter_obj, tstart, tend, include_temporary=False, include_averages=True):
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
				print "ModelRegistry lookup failed for ", sys, subsys
				continue
			# get the corresponding model class
			model = get_registered_model(m.model_class)
			filter_kwargs = {}
			# filter by header and value
			for h, vals in specs.get('series').iteritems():
				param = h + '__in' # django syntax for "all values in a given list"
								   # for example, objects.filter(Name__in=["foo", "bar"])
				filter_kwargs[param] = vals
			if not (include_temporary or include_averages):
				raise AssertionError("series must include either temporary or average values")
			elif include_temporary and include_averages:
				pass # just don't filter at all
			elif include_temporary:
				filter_kwargs['temporary'] = True
			elif include_averages:
				filter_kwargs['temporary'] = False
			# make the query according to all given filters
			Q = model.objects.filter(Time__gte=tstart, Time__lt=tend, **filter_kwargs)
			# filter for only the selected columns
			# note that if 'columns' is None or [], no filtering is performed and all columns are returned
			data_columns = specs.get('columns')
			if data_columns:
				all_columns = data_columns[:]
				for head in model.get_header_names():
					if head not in all_columns:
						all_columns.append(head)
			else:
				data_columns = model.get_field_names()
				all_columns = model.get_header_names() + model.get_field_names()
			Q = Q.values(*all_columns)
			retlist.extend(__obj_list_to_hd_dict(Q, model, data_columns))
	return retlist

def live_filter(filter_obj):
	"""see series_filter for api (identical)"""
	retlist = []
	for sys, subs in filter_obj.iteritems():
		for subsys, specs in subs.iteritems():
			# look up the requested system in our registry
			m = ModelRegistry.objects.get(system=sys, short_name=subsys)
			# if it doesn't exist, skip this one
			if not m: continue
			# get the corresponding model class
			model = get_registered_model(m.model_class)
			# the relevant queryset is all rows which share this most-recent timestamp
			new_data = model.objects.filter(Time=model.latest(temporary=True))
			# use the series filters
			for h, vals in specs.get('series').iteritems():
				new_data = filter(lambda obj: vars(obj).get(h) in vals, new_data)
			data_columns = specs.get('columns')
			if not data_columns:
				data_columns = model.get_field_names()
			retlist.extend(__obj_list_to_hd_dict([vars(d) for d in new_data], model, data_columns))
	return retlist