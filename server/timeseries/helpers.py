from timeseries.models import ModelRegistry
import dateutil.parser
from dateutil.tz import tzlocal
import operator

# refer to https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types
model_types = {
	'numeric' : [u'FloatField', u'IntegerField', u'BigIntegerField', u'DecimalField', u'PositiveIntegerField', u'PositiveSmallIntegerField', u'SmallIntegerField' ],
	'string' : [u'CharField', u'BooleanField', u'TextField']
}

def systems_schema():
	"""construct and return a list of json objects describing the different systems with available timeseries data. Note that no actual data is returned.
	A 'system' is something like 'HVAC' or 'Electric', and a subsystem is, for example, VRF within HVAC.
	Some system have 'indexes'. These are columns which further differentiate within a subsystem. For example, the HVAC system has an index for rooms; there
	is one entry per timestamp per room. `indexes` may be empty in some systems.

	structure is as follows:
	[
		{
			system: 'System Name',
			subsystem: 'Subsystem Name',
			id : 'CamelCaseId',
			description : 'this is a really fancy and efficient subsystem',
			status : 0, // 0, 1, or 2. see timeseries.models.ModelRegistry for what they mean.
			numeric : [('NumericColumn1', 'readable name'), ('NumericColumn2', 'readable name'), ...],
			string  : [('NonNumericColumnA', 'readable name'), ('NonNumericColumnB', 'readable name'), ...],
			indexes : [(id,'readable name'), (id, 'readable name'), ...]
			units : {
				'ColumnName1' : 'in',
				'ColumnName2' : 'kWh'
		}, ...
	]
	"""
	return (registry.schema() for registry in ModelRegistry.objects.all())

def split_on_indexes(queryset, column_filter=None, isoformat=False):
	"""given a queryset of TimeseriesBase objects, return a dict mapping from each unique index to the list of
	objects which share that index

	column_filter behaves like QuerySet.values(); instead of a list of objects, a list of object-like dictionaries will be returned"""
	index_lookup = {}
	for obj in queryset:
		ind = obj.index_tuple() # index_tuple() method is defined in TimeseriesBase. May be None.
		filtered_obj_dict = vars(obj) if not column_filter else dict((key, vars(obj)[key]) for key in column_filter)
		if isoformat:
			filtered_obj_dict['Time'] = filtered_obj_dict['Time'].isoformat()
		index_lookup[ind] = index_lookup.get(ind, []) + [filtered_obj_dict] # append the current object to this list
	# sort data by time
	for index, data in index_lookup.iteritems():
		data.sort(key=operator.itemgetter('Time'))
	return index_lookup

def field_name_tuples(fields_list, registry):
	db_names = [f.get_attname() for f in fields_list]
	# TODO relate this to Max's metadata table. something like this:
	# readable = [Metadata.objects.get(model=registry, field=dbname).humanname for dbname in db_names]
	readable = [f.verbose_name or f.name for f in fields_list]
	return zip(db_names, readable)

def timedelta_seconds(timedelta):
	"""get the total seconds in a timedelta object.

	the built-in timedelta.total_seconds() function appears first in Python 2.7. The server runs 2.6.
	"""
	return timedelta.days * 86400 + timedelta.seconds

def memoized(fn):
	"""decorator to cache function results"""
	cache = {}
	def fn_wrapper(*args):
		a = tuple(args)
		if a not in cache:
			cache[a] = fn(*args)
		return cache[a]
	return fn_wrapper

@memoized
def get_registered_model(class_path):
	"""given the import path for a model (e.g. ModelRegistry.model_class), return the model class"""
	path_parts = class_path.split('.')
	module_path = '.'.join(path_parts[:-1])
	class_name = path_parts[-1]
	mod = __import__(module_path, globals(), locals(), [class_name])
	return getattr(mod, class_name)

@memoized
def get_registered_scraper(scraper_path):
	"""given the import path for a scraper (e.g. ModelRegistry.scraper_class), return the scraper class"""
	path_parts = scraper_path.split('.')
	module_path = '.'.join(path_parts[:-1])
	class_name = path_parts[-1]
	mod = __import__(module_path, globals(), locals(), [class_name])
	return getattr(mod, class_name)

def parse_time(isostring):
	"""Parse an ISO datetime string into a datetime object. If no timezone information is given it's assumed to be local"""
	dt = dateutil.parser.parse(isostring)
	if dt.tzinfo == None: # if it's a naive datetime
		dt = dt.replace(tzinfo=tzlocal())
	return dt

def __query_data(sys, subsys, model, filter_kwargs, columns, isoformat=False):
	"""this private function handles the output formatting specified by series_filter
	"""
	# make the query according to all given filters
	Q = model.objects.filter(**filter_kwargs)
	Q = Q.select_related() # follow foreign key references
	indexes_split = split_on_indexes(Q, column_filter=columns, isoformat=isoformat)

	return [{
			'system' : sys,
			'subsystem' : subsys,
			'index' : idx[1] if idx else None,
			'data' : objects
			} for idx, objects in indexes_split.iteritems()]

def series_filter(filter_objs, tstart, tend, include_temporary=False, include_averages=True, isoformat=False):
	"""Given the definition of some serieses, return a list of dicts with the data.

	filter definition is as follows:
	[
		{
			system: 'system name',
			subsystem: 'subsystem name', 
			indexes : [id1, id2, id3, ...],
			columns : ['ColumnName1', 'ColumnName2']
		}, ...
	]

	returned data is in this format:
	[
		{
			system: 'system name',
			subsystem: 'subsystem name',
			index: 'index name',
			data: [	{Time: 'ISO Time 1', 'ColumnName1': value1, 'ColumnName2: value2'},
					{Time: 'ISO Time 2', 'ColumnName1': value1, 'ColumnName2: value2'}, ...]
		}, ...
	]
	"""
	retlist = []
	for specs in filter_objs:
		sys = specs.get('system')
		subsys = specs.get('subsystem')
		# lookup the registered sys/subsys pair in the registry
		reg = ModelRegistry.objects.get(system=sys, short_name=subsys)
		# if it doesn't exist, skip this one
		if not reg:
			print "ModelRegistry lookup failed for ", sys, subsys
			continue
		# get the corresponding model class
		model = get_registered_model(reg.model_class)
		# build the queryset filter
		filter_kwargs = {}
		# filter by index
		idx_col = model.get_index_column()
		if idx_col:
			filter_kwargs['%s__in' % idx_col] = specs.get('indexes')
		if not (include_temporary or include_averages):
			raise AssertionError("series must include either temporary or average values")
		elif include_temporary and include_averages:
			pass # just don't filter at all
		elif include_temporary:
			filter_kwargs['temporary'] = True
		elif include_averages:
			filter_kwargs['temporary'] = False

		# filter for only the selected columns
		columns = specs.get('columns')
		if not columns: continue
		if 'Time' not in columns:
			columns.insert(0, 'Time')

		filter_kwargs['Time__gte'] = tstart
		filter_kwargs['Time__lt']  = tend

		retlist.extend(__query_data(sys, subsys, model, filter_kwargs, columns, isoformat))

	return retlist

def live_filter(filter_objs, isoformat=False):
	"""see series_filter for api (identical). instead of returning data across a timespan, this returns only the latest point for each series"""
	retlist = []
	for specs in filter_objs:
		sys = specs.get('system')
		subsys = specs.get('subsystem')
		# look up the requested system in our registry
		m = ModelRegistry.objects.get(system=sys, short_name=subsys)
		# if it doesn't exist, skip this one
		if not m:
			print "ModelRegistry lookup failed for ", sys, subsys
			continue
		# get the corresponding model class
		model = get_registered_model(m.model_class)

		# filter for only the selected columns
		columns = specs.get('columns')
		if not columns: continue
		if 'Time' not in columns:
			columns.insert(0, 'Time')

		# the relevant queryset is all rows which share this most-recent timestamp.
		# non-temporary vals are averages, and we don't want those live.
		filter_kwargs = {'Time' : model.latest(temporary=True)}

		retlist.extend(__query_data(sys, subsys, model, filter_kwargs, columns, isoformat))
	return retlist