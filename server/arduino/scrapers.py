import requests
import time
import datetime
import pytz
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
			ok = 0
			js = requests.get('http://%s/%d' % (self.ip, time.time()), timeout=5.0).json()
			for pointname, info in js.iteritems():
				t = info['t'] # time
				if t is 0: continue # sensor initialized but hasn't stored a valid data point yet
				v = info['v'] # value
				aware_datetime = pytz.UTC.localize(datetime.datetime.utcfromtimestamp(t))
				m = SensorDataPoint(sensor=self._registry, name=pointname, Time=aware_datetime)
				if type(v) == str:
					m.svalue = v
				elif type(v) == float:
					m.fvalue = v
				elif type(v) == int:
					m.ivalue = v
				else: continue
				ok += 1
				models.append(m)
			if ok == len(js.keys()):
				self.status_ok()
			else:
				self.status_format_error()
		except requests.exceptions.RequestException:
			self.status_comm_error()
		except:
			self.status_format_error()
		finally:
			return models