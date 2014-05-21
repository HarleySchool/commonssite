from django.db import models
import re
import datetime
import pytz

class TimeseriesBase(models.Model):
	'''The minimum structure of a timeseries model. Other time-logging models should inherit from this class.
	'''
	Time = models.DateTimeField(db_column='time')
	temporary = models.BooleanField(default=False) # whether or not this entry will be removed after a set time

	@classmethod
	def remove_expired(cls, timespan=datetime.timedelta(hours=24)):
		"""Remove all entries tagged with `temporary` and that are older than (now - timespan)
		"""
		now = pytz.UTC.localize(datetime.datetime.utcnow())
		earliest = now - timespan
		query = cls.objects.filter(Time__lt=earliest, temporary=True)
		query.delete() # this call immediately hits the database and removes all the entries in the queryset

	@classmethod
	def get_field_names(cls):
		"""Return all field names but none of the header names
		"""
		fields = []
		if hasattr(cls, "_meta"):
			if hasattr(cls._meta, "fields"):
				fields = [field.get_attname() for field in cls._meta.fields]
		for head in cls.get_index_column():
			fields.remove(head)
		if u'id' in fields:
			fields.remove(u'id')
		if u'temporary' in fields:
			fields.remove(u'temporary')
		return fields

	@classmethod
	def get_index_column(cls):
		"""Return the column names which are unique together (together they act as a unique identifier for a row)
		"""
		# unique_together is a tuple of tuples, e.g. (('Time', 'System'),)
		if hasattr(cls, "_meta"):
			if hasattr(cls._meta, "unique_together"):
				if len(cls._meta.unique_together) > 0:
					try:
						unq = list(cls._meta.unique_together[0])
						unq.remove('Time')
						return unq[0]
					except:
						pass
		return None

	@classmethod
	def latest(cls, temporary=None):
		"""return a datetime object that is the timestamp of the most recent entries in this table
		"""
		if temporary is None:
			return (cls.objects.order_by('-Time')[0]).Time
		else:
			return (cls.objects.filter(temporary=temporary).order_by('-Time')[0]).Time

	def index(self):
		"""return a tuple of index (header) values for this object
		"""
		col = self.get_index_column()
		if col:
			obj_dict = vars(self)
			return obj_dict[col]
		else:
			return None

	@classmethod
	def index_value_tuples(cls, queryset_latest=None):
		"""construct a list of tuples (id,name) for this model's index (or empty list if no index)
		"""
		# ideally the queryset is passed in so it can be reused
		if not queryset_latest:
			queryset_latest = cls.objects.filter(Time=cls.latest())
		# start with blank list (default)
		indexes = []
		index_column = cls.get_index_column()
		if index_column:
			# we want to build up a parallel array of index ids/names.
			# for example if index_values is [1,2,3] then index_names could be ["Circuit 1", "Outlets", "another circuit"]
			# such that zip(index_values, index_names) forms pairings of indexes and names
			index_ids = [obj.index() for obj in queryset_latest]
			# check if it's a foreign key
			if cls._meta.get_field_by_name(index_column).rel:
				# look up the ForeignKey's Model
				foreignkey_table = cls._meta.get_field_by_name(index_column).related.parent_model
				# this lambda function maps from an object to the string value of its' ForeignKey index
				name_getter = lambda obj: str(foreignkey_table.objects.get(id=vars(obj)[index_column]))
			else:
				# if not a foreign key, then just use the plain ol' index value
				name_getter = lambda obj: str(vars(obj)[index_column])
			# create list of names
			index_names = map(name_getter, queryset_latest)
			# zip together ids and names
			indexes = zip(index_ids, index_names)
		return indexes

	class Meta:
		abstract = True

class ModelRegistry(models.Model):
	'''This table keeps track of registered timeseries models and related information'''

	# see timeseries.scrapers.ScraperBase.get_and_save_single
	# for an example of how these are used
	STATUS_CHOICES = (
		(2, 'Communication Error'),
		(1, 'Formatting Error'),
		(0, 'OK'))
	
	__regex_non_char = re.compile(r'[^a-zA-Z]+')

	system = models.CharField(max_length=16)
	short_name = models.CharField(max_length=32) # aka subsystem
	description = models.TextField()
	status = models.IntegerField(choices=STATUS_CHOICES) # latest status of this model's scraper
	model_class = models.CharField(max_length=64)
	scraper_class = models.CharField(max_length=64, null=True)

	def __unicode__(self):
		return unicode(self.short_name)

	def make_id(self):
		"""Convert the short_name into an HTML-usable id (no spaces or special characters)
		"""
		# a regualar expression to capture a sequence of non-letter characters
		words = ModelRegistry.__regex_non_char.split(self.short_name)
		caps = [w.capitalize() for w in words]
		return ''.join(caps)

	def schema(self):
		"""create a dictionary representation of this registry's model's schema (see timeseries.helpers.systems_schema)"""
		from timeseries import helpers as h
		model = h.get_registered_model(self.model_class)
		# break fields up into numeric and string types
		# (note that some types aren't covered in either numeric or string, like AutoField, ForeignKey, etc..
		# these are for data columns only)
		fields = model._meta.fields
		numeric_fields = filter(lambda f: f.get_internal_type() in h.model_types['numeric'], fields)
		string_fields  = filter(lambda f: f.get_internal_type() in h.model_types['string'], fields)
		schema = {
			'system' : self.system,
			'subsystem' : self.short_name,
			'indexes' : model.index_value_tuples(),
			'id' : self.make_id(),
			'status' : self.status,
			'numeric' : h.field_name_tuples(numeric_fields),
			'string' : h.field_name_tuples(string_fields),
			'units' : {} # TODO
		}
		return schema