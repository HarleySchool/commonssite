import requests, json
from commonssite.settings import sma_host, sma_port, sma_password
from commonssite.scrapers.template import ScraperTemplate

# NOTE: THE FORMAT OF THE DATA IN THIS FILE COMES FROM
# A TECHNICAL DOCUMENT RELEASED BY SMA CALLED
# 'REMOTE PROCEDURE CALL DESCRIPTION INTERFACES AND API DEFINITION'

devices = {
	'weather' : {
		'key' : 'SENS0700:26877',
		'name' : 'SMA Weather Sensor',
		'channels' : 'null',
		'children' : 'null'
	},
	'power' : {
		'key' : 'WRHV5K84:19120146',
		'name' : 'SMA Solar Data',
		'channels' : 'null',
		'children' : 'null'
	}
}

class ScraperSolar(ScraperTemplate):

	def __init__(self):
		ScraperTemplate.__init__(self, "solar")

	def _MD5Hash(self, s):
		import md5
		m = md5.new()
		m.update(s)
		return m.hexdigest()

	def _emptyDevObject(self):
		"""Creates a template JSON object (a python dict actually) according to
		the schema for a Device Object defined in section 6.1 of the RPC manual
		"""
		return {
			"key" : None,
			"name" : None,
			"channels" : None,
			"children" : None
		}

	def _emptyChannelObject(self):
		return {
			"meta" : None, # must be set
			"name" : None,
			"value" : None, # must be set
			"unit" : None,
			"min" : None,
			"max" : None,
			"options" : None
		}

	def _emptyRpcObject(self):
		"""Creates a template JSON object (a python dict actually) according to
		the schema for an RPC request defined in section 4.1 of the RPC manual
		"""
		return {
			'version' : '1.0',
			'proc' : '', # set by procedure functions
			'id' : '0',  # should probably set something smart
			'format' : 'JSON',
			'passwd' : self._MD5Hash(sma_password),
			'params' : {}
		}

	def _doGetPlantOverview(self):
		rpc = self._emptyRpcObject()
		rpc["proc"] = "GetPlantOverview"
		rpc["id"] = "1"
		return self._postRequest(rpc)

	def _doGetDevices(self):
		rpc = self._emptyRpcObject()
		rpc["proc"] = "GetDevices"
		rpc["id"] = "2"
		return self._postRequest(rpc)

	def _doGetChannels(self, dev_obj):
		rpc = self._emptyRpcObject()
		rpc["proc"] = "GetProcessDataChannels"
		rpc["id"] = "3"
		rpc["params"] = {
			"device" : dev_obj['key']
		}
		return self._postRequest(rpc)

	def _doGetData(self, dev_objects):
		rpc = self._emptyRpcObject()
		rpc["proc"] = "GetProcessData"
		rpc["id"] = "4"
		rpc["params"] = {
			# dev_objects must be an array containing dicts with "key" and "channels"
			"devices" : dev_objects
		}
		return self._postRequest(rpc)

	def _postRequest(self, body={}):
		req = requests.post('http://%s:%d/rpc' % (sma_host, sma_port), data="RPC=%s" % json.dumps(body))
		return req.text

	def get_data(self):
		return []

if __name__ == '__main__':
	obj = ScraperSolar()
	from pprint import pprint
	pprint(json.loads(obj._doGetData([devices['power']])))