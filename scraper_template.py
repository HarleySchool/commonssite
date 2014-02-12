class DataScraper(object):
	"""
	Each of the subsystems of commons data collection (i.e. hvac, solar, veris...) is an extension of this class
	"""
	def __init__(self, name):
		self.table_name = name

	def get_name(self):
		return self.table_name

	def get_data(self):
		"""
		this is implemented by each sub class separately and should return a dict with the following format:

		data = {
			"field1" : {
				time0 : value0,
				time1 : value1,
			},
			"field2" : {
				time0 : value0,
				time1 : value1
			},
			... etc
		}
		data = {
			time0 : {
				field1 : value1,
				field2 : value2
			}
		}
		"""
		return {} # default. should be overriden

	def write_sql(self):
		pass