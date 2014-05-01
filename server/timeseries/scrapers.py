import time
import requests

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

	def get_and_save_single(self):
		try:
			for new_data in self.get_data():
				new_data.temporary = True
				new_data.save(force_insert=True)
			print '=================='
			print '%s done at %s' % (self.__class__.__name__, time.time())
			self._registry.status = 2 # 2 means 'OK'
		except requests.exceptions.ConnectionError:
			# what happens when the requests library fails
			self._registry.status = 1 # 1 means 'Connection Down'
		except Exception:
			# catch-all for other problems
			self._registry.status = 0 # 0 means 'Communication Error'
		finally:
			self._registry.save() # update status in the database


	def get_data(self):
		"""Return a list of TimeseriesBase (subclass) models
		"""
		return []