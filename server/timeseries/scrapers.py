import time

class ScraperBase(object):
	"""A scraper base class which takes care of shared functionality

	The old scraping method worked by keeping a schedule of tasks and executing a scraper every 20 minutes or so.
	This version works by logging new data as frequently as possible (tagged with temporary=True), and then later
	using mark_latest_as_permanent() to save data points permanently.
	"""

	def __init__(self, model_class, registry_instance):
		self._model = model_class
		self._registry = registry_instance

	def mark_latest_as_permanent(self):
		"""Mark the last-saved entry for permanent storage. Also cleans up expired temporary entries.
		"""
		queryset = self._model.objects.filter(Time=self._model.latest())
		queryset.update(temporary=False) # update all the 'latest' rows as permanent
		# this method is called infrequently (~20 minutes). Use this opportunity to release old objects
		self._model.remove_expired()

	def status_ok(self):
		self._registry.status = 2

	def status_format_error(self):
		self._registry.status = 1

	def status_comm_error(self):
		self._registry.status = 0

	def get_and_save_single(self):
		try:
			for new_data in self.get_data():
				new_data.temporary = True
				new_data.save(force_insert=True)
			print '=================='
			print '%s done at %s' % (self.__class__.__name__, time.time())
		except:
			self.status_comm_error()
		finally:
			self._registry.save() # update status in the database

	def get_data(self):
		"""Return a list of TimeseriesBase (subclass) models. get_data must be implemented by subclasses of ScraperBase
		"""
		self.status_comm_error()
		return []