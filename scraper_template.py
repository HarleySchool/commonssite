class ScraperTemplate(object):
	"""
	Each of the subsystems of commons data collection (i.e. hvac, solar, veris...) is an extension of this class.
	Subclasses must define a name in __init__ and must override get_data. Writing to SQL is handled by this parent class.
	"""
	def __init__(self, name):
		"""Initialize this scraper class to use the SQL table <name>
		"""
		self.table_name = name

	def get_name(self):
		return self.table_name

	def get_data(self):
		"""
		this is implemented by each sub class separately and should return a list of data objects with the following format.
		If multiple timestamps are available, that is simply more elements in the list!

		data = [{
					"timestamp" : UTC-time,
					"field1" : value1,
					"field2" : value2,
					... etc
				}]
		"""
		return [] # default. should be overriden

	def write_sql(self):
		name = self.get_name()
		for datarow in self.get_data():
			# insert the row
			pass