import time

class ScraperBase(object):
	"""A scraper base class which takes care of shared functionality

	The old scraping method worked by keeping
	"""

	@classmethod
	def mark_latest_as_permanent(cls):
		latest = cls.objects.order_by('-Time')[0]
		latest.temporary = False
		latest.save() # performs a SQL UPDATE

	@classmethod
	def name(cls):
		return cls.__name__

	def get_and_save_single(self):
		for new_data in self.get_data():
			new_data.temporary = True
			new_data.save(force_insert=True)
		print '=================='
		print '%s done at %s' % (self.name(), time.time())

	def get_data():
		"""Return a list of TimeseriesBase (subclass) models
		"""
		return []