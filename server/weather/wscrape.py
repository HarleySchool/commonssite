import datetime
import pytz
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(BASE_DIR, 'weather'))
from weewx.drivers.vantage import Vantage
from commonssite.server.weather.models import weatherdata

class Weather():
	def __init__(self):
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
			'yearET': 'yearet'
	}

	def doParse(self, data):
		parsed = {}
		for key, val in self.dict_key_map.iteritems():
			parsed[val] = data[key]
		return parsed

	def get_data(self):
		v = Vantage(type='ethernet', host='10.1.6.203')
		data = next(v.genDavisLoopPackets())
		parsed = self.doParse(data)
		now = pytz.UTC.localize(datetime.datetime.utcnow())
		model = weatherdata(Time=now, **parsed)
		return [model]

if __name__ == '__main__':
	w = Weather()
	m = w.get_data()
	m.save(force_insert=True)
	print 'done'