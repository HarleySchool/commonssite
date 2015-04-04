import requests
import time
import datetime
import pytz
from timeseries.scrapers import ScraperBase
from arduino.models import GreenhouseDHT#, SensorDataPoint


class GreenhouseScraper(ScraperBase):

	__greenhouse_ip = '10.1.6.204'

	@staticmethod
	def __map_response_to_model(json_name):
		mapping = {	"HUM_EAST_CHIMNEY_LOW" : "hum_east_chimney_low",
					"TEMP_EAST_CHIMNEY_LOW" : "temp_east_chimney_low",
					"HUM_EAST_CHIMNEY_HIGH" : "hum_east_chimney_high",
					"TEMP_EAST_CHIMNEY_HIGH" : "temp_east_chimney_high",
					"HUM_WEST_CHIMNEY_LOW" : "hum_west_chimney_low",
					"TEMP_WEST_CHIMNEY_LOW" : "temp_west_chimney_low",
					"HUM_WEST_CHIMNEY_HIGH" : "hum_west_chimney_high",
					"TEMP_WEST_CHIMNEY_HIGH" : "temp_west_chimney_high",
					"HUM_GREENHOUSE_LOW" : "hum_greenhouse_low",
					"TEMP_GREENHOUSE_LOW" : "temp_greenhouse_low",
					"HUM_MEZZANINE" : "hum_mezzanine",
					"TEMP_MEZZANINE" : "temp_mezzanine",
					"HUM_GREENHOUSE_HIGH" : "hum_greenhouse_high",
					"TEMP_GREENHOUSE_HIGH" : "temp_greenhouse_high"}
		return mapping.get(json_name)

	def get_data(self):
		models = []
		try:
			js = requests.get('http://%s/%d' % (GreenhouseScraper.__greenhouse_ip, time.time()), timeout=1.0)
			latest_time = None
			model_kwargs = {}
			for pointname, info in js.json().iteritems():
				t = info['t'] # time
				if t is 0: continue # sensor initialized but hasn't stored a valid data point yet
				aware_datetime = pytz.UTC.localize(datetime.datetime.utcfromtimestamp(t))
				latest_time = aware_datetime if latest_time is None else max(latest_time, aware_datetime)
				model_kwargs[self.__map_response_to_model(pointname)] = info['v']
			m = GreenhouseDHT(Time=aware_datetime, **model_kwargs)
			models.append(m)
			self.status_ok()
		except requests.exceptions.RequestException as e:
			print e
			self.status_comm_error()
		except Exception as e:
			print e
			self.status_format_error()
		finally:
			return models


# class NetworkSensorScraper(ScraperBase):

# 	def __init__(self, model, registry_instance):
# 		super(NetworkSensorScraper, self).__init__(model, registry_instance)
# 		# all NetworkSensors are registered to the 'Arduino' system
# 		# and the 'Name@IP' subsystem. Here we parse out that IP address
# 		self.ip = registry_instance.short_name.split('@')[1]

# 	def get_data(self):
# 		models = []
# 		try:
# 			ok = 0
# 			js = requests.get('http://%s/%d' % (self.ip, time.time()), timeout=5.0).json()
# 			for pointname, info in js.iteritems():
# 				t = info['t'] # time
# 				if t is 0: continue # sensor initialized but hasn't stored a valid data point yet
# 				v = info['v'] # value
# 				aware_datetime = pytz.UTC.localize(datetime.datetime.utcfromtimestamp(t))
# 				m = SensorDataPoint(sensor=self._registry, name=pointname, Time=aware_datetime)
# 				if type(v) == str:
# 					m.svalue = v
# 				elif type(v) == float:
# 					m.fvalue = v
# 				elif type(v) == int:
# 					m.ivalue = v
# 				else: continue
# 				ok += 1
# 				models.append(m)
# 			if ok == len(js.keys()):
# 				self.status_ok()
# 			else:
# 				self.status_format_error()
# 		except requests.exceptions.RequestException:
# 			self.status_comm_error()
# 		except:
# 			self.status_format_error()
# 		finally:
# 			return models
