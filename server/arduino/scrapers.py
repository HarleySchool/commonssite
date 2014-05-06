import requests
import time
import datetime
from timeseries.scrapers import ScraperBase
from arduino.models import SensorDataPoint

class NetworkSensorScraper(ScraperBase):

	def __init__(self, model, registry_instance):
		super(NetworkSensorScraper, self).__init__(model, registry_instance)
		# all NetworkSensors are registered to the 'Arduino' system
		# and the 'Name@IP' subsystem. Here we parse out that IP address
		self.ip = registry_instance.short_name.split('@')[1]

	def get_data(self):
		models = []
		try:
			js = requests.get('http://%s/%d' % (self.ip, time.time())).json()
			for pointname, info in js.iteritems():
				t = info['t'] # time
				if t is 0: continue # sensor initialized but hasn't stored a valid data point yet
				v = info['v'] # value
				m = SensorDataPoint(sensor=self._registry, name=pointname, Time=datetime.datetime.utcfromtimestamp(t))
				if type(v) == str:
					m.svalue = v
				elif type(v) == float:
					m.fvalue = v
				elif type(v) == int:
					m.ivalue = v
				else:
					continue
				models.append(m)
			self.status_ok()
		except requests.exceptions.ConnectionError:
			self.status_comm_error()
		except:
			self.status_format_error()
		finally:
			return models