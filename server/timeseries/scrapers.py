
class ScraperBase(object):
	"""A scraper base class which takes care of shared functionality

	The old scraping method worked by keeping
	"""

	@classmethod
	def mark_latest_as_permanent(cls):
		latest = cls.objects.order_by('-Time')[0]
		latest.temporary = False
		latest.save() # performs a SQL UPDATE

	def get_data():
		"""Return a list of TimeseriesBase (subclass) models
		"""
		return []