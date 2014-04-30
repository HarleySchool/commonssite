import time

class ScraperBase(object):
	"""A scraper base class which takes care of shared functionality

	The old scraping method worked by keeping a schedule of tasks and executing a scraper every 20 minutes or so.
	This version works by logging new data as frequently as possible (tagged with temporary=True), and then later
	using mark_latest_as_permanent() to save data points permanently.
	"""

	def __init__(self, model_class):
		self._model = model_class

	def mark_latest_as_permanent(self):
		"""Mark the last-saved entry for permanent storage. Also cleans up expired temporary entries.
		"""
		queryset = self._model.objects.filter(Time=self._model.latest())
		queryset.update(temporary=False) # update all the 'latest' rows as permanent
		# this method is called infrequently (~20 minutes). Use this opportunity to release old objects
		self._model.remove_expired()

	def get_and_save_single(self):
		for new_data in self.get_data():
			new_data.temporary = True
			new_data.save(force_insert=True)
		print '=================='
		print '%s done at %s' % (self.__class__.__name__, time.time())

	def get_data(self):
		"""Return a list of TimeseriesBase (subclass) models
		"""
		return []