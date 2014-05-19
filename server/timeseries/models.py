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
		for h in cls.get_header_names():
			fields.remove(h)
		if u'id' in fields:
			fields.remove(u'id')
		if u'temporary' in fields:
			fields.remove(u'temporary')
		return fields

	@classmethod
	def get_header_names(cls):
		"""Return the column names which are unique together (together they act as a unique identifier for a row)
		"""
		# unique_together is a tuple of tuples, e.g. (('Time', 'System'),)
		if hasattr(cls, "_meta"):
			if hasattr(cls._meta, "unique_together"):
				if len(cls._meta.unique_together) > 0:
					return [f.get_attname() for f in cls._meta.fields if f.name in list(cls._meta.unique_together[0])]
		return ['Time']

	@classmethod
	def get_series_identifiers(cls):
		"""Return a list of dicts, where each is a unique combination of header:value for all of the headers
		"""
		all_headers = cls.get_header_names()
		all_headers.remove('Time')
		return list(cls.objects.values(*all_headers).distinct())

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
		vals = [vars(self)[head] for head in self.get_header_names() if head != 'Time']
		return tuple(vals) 

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
