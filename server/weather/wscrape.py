import datetime
from timeseries.scrapers import ScraperBase
from commonssite.settings import weather_host
import pytz
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(BASE_DIR, 'weather'))
from weewx.drivers.vantage import Vantage
from commonssite.server.weather.models import WeatherData

class Weather(ScraperBase):
	
	def __init__(self, model):
		super(Weather, self).__init__(model)
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
		self.v = Vantage(type='ethernet', host=weather_host)

	def doParse(self, data):
		parsed = {}
		for key, val in self.dict_key_map.iteritems():
			parsed[val] = data[key]
		return parsed

	def get_data(self):
		data = next(self.v.genDavisLoopPackets())
		parsed = self.doParse(data)
		now = pytz.UTC.localize(datetime.datetime.utcnow())
		model = WeatherData(Time=now, **parsed)
		return [model]

if __name__ == '__main__':
	from pprint import pprint
	w = Weather()
	data = w.doParse(next(w.v.genDavisLoopPackets()))
	pprint(data)