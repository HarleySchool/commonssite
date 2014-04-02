from django.db import models

class TimeseriesBase(models.Model):
	'''The minimum structure of a timeseries model. Other time-logging models should inherit from this class.
	'''
	Time = models.DateTimeField(db_column='time')

	@classmethod
	def get_field_names(cls):
		"""Return all field names but none of the header names
		"""
		fields = []
		if hasattr(cls, "_meta"):
			if hasattr(cls._meta, "fields"):
				fields = [field.name for field in cls._meta.fields]
		for h in cls.get_header_names():
			fields.remove(h)
		if u'id' in fields:
			fields.remove(u'id')
		return fields

	@classmethod
	def get_header_names(cls):
		"""Return the column names which are unique together (together they act as a unique identifier for a row)
		"""
		# unique_together is a tuple of tuples, e.g. (('Time', 'System'),)
		if hasattr(cls, "_meta"):
			if hasattr(cls._meta, "unique_together"):
				return list(cls._meta.unique_together[0])
		else:
			return ['Time']

	class Meta:
		abstract = True

""" RUNTIME MODULE LOADER
def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
"""	

class ModelRegistry(models.Model):
	'''This table keeps track of registered timeseries models and related information'''
	system = models.CharField(max_length=16)
	model_class = models.CharField(max_length=64)
	scraper_class = models.CharField(max_length=64, null=True)
	description = models.TextField()
	short_name = models.CharField(max_length=32)

	def __unicode__(self):
		return unicode(self.short_name)
