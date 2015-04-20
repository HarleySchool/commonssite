import datetime
from timeseries.scrapers import ScraperBase
from commonssite.settings import weather_host
from timeseries.models import ModelRegistry
import pytz
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(BASE_DIR, 'weather'))
from weewx.drivers.vantage import Vantage
import weewx
from commonssite.server.weather.models import WeatherData

class Weather(ScraperBase):
	
	def __init__(self, model, registry_instance):
		super(Weather, self).__init__(model, registry_instance)
		self.dict_key_map = {
			'UV' : 'uv',
			'barometer' : 'barometer',
			'dayET' : 'dayet',
			'dayRain' : 'dayrain',
			'dewpoint' : 'dewpoint',
			'heatindex' : 'heatindex',
			'inHumidity' : 'inhumidity',
			'inTemp' : 'intemp',
			'monthET': 'monthet',
			'monthRain' : 'monthrain',
			'outHumidity': 'outhumidity',
			'outTemp': 'outtemp',
			'radiation': 'radiation',
			'rain': 'rain',
			'rainRate': 'rainrate',
			'stormRain': 'stormrain',
			'stormStart': 'stormstart',
			'sunrise' : 'sunrise',
			'sunset' : 'sunset',
			'windDir': 'winddir',
			'windSpeed': 'windspeed',
			'windchill': 'windchill',
			'yearET': 'yearet',
			'yearRain' : 'yearrain'
		}
		self.v = None

	def doParse(self, data):
		parsed = {}
		for key, val in self.dict_key_map.iteritems():
			parsed[val] = data[key]
		return parsed

	def connect(self):
		if self.v is None:
			self.v = Vantage(type='ethernet', host=weather_host, max_retries=2, wait_before_retry=2.4)

	def get_data(self):
		try:
			self.connect()
			data = next(self.v.genDavisLoopPackets())
			parsed = self.doParse(data)
			now = pytz.UTC.localize(datetime.datetime.utcnow())
			model = WeatherData(Time=now, **parsed)
			self.status_ok()
			return [model]
		except weewx.WakeupError:
			print "Weather parser wakeup issues. resetting connection."
			self.v.closePort()
			self.v = Vantage(type='ethernet', host=weather_host, max_retries=4, wait_before_retry=2.0)
			self.status_comm_error()
		except Exception as e:
			print "Weather parser error:"
			print e
			# any other exception implies that the transaction took place but we weren't able to parse it
			self.status_format_error()
		return []

if __name__ == '__main__':
	from pprint import pprint
	r = ModelRegistry.objects.get(short_name='Weather')
	w = Weather(WeatherData,r)
	data = w.doParse(next(w.v.genDavisLoopPackets()))
	pprint(data)
	w.v.closePort()
	w.v = Vantage(type='ethernet',host=weather_host, max_retries=4, wait_before_retry=2.0)
