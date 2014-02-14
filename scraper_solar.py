import requests, json
from settings import sma_host, sma_port, sma_password
from scraper_template import ScraperTemplate

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
		ScraperTemplate.__init__("Solar")

	def _MD5Hash(s):
		import md5
		m = md5.new()
		m.update(s)
		return m.hexdigest()

	def _emptyDevObject():
		"""Creates a template JSON object (a python dict actually) according to
		the schema for a Device Object defined in section 6.1 of the RPC manual
		"""
		return {
			"key" : None,
			"name" : None,
			"channels" : None,
			"children" : None
		}

	def _emptyChannelObject():
		return {
			"meta" : None, # must be set
			"name" : None,
			"value" : None, # must be set
			"unit" : None,
			"min" : None,
			"max" : None,
			"options" : None
		}

	def _emptyRpcObject():
		"""Creates a template JSON object (a python dict actually) according to
		the schema for an RPC request defined in section 4.1 of the RPC manual
		"""
		return {
			'version' : '1.0',
			'proc' : '', # set by procedure functions
			'id' : '0',  # should probably set something smart
			'format' : 'JSON',
			'passwd' : ScraperSolar._MD5Hash(sma_password),
			'params' : {}
		}

	def _doGetPlantOverview():
		rpc = ScraperSolar._emptyRpcObject()
		rpc["proc"] = "GetPlantOverview"
		rpc["id"] = "1"
		return ScraperSolar._postRequest(rpc)

	def _doGetDevices():
		rpc = ScraperSolar._emptyRpcObject()
		rpc["proc"] = "GetDevices"
		rpc["id"] = "2"
		return ScraperSolar._postRequest(rpc)

	def _doGetChannels(dev_obj):
		rpc = ScraperSolar._emptyRpcObject()
		rpc["proc"] = "GetProcessDataChannels"
		rpc["id"] = "3"
		rpc["params"] = {
			"device" : dev_obj['key']
		}
		return ScraperSolar._postRequest(rpc)

	def _doGetData(dev_objects):
		rpc = ScraperSolar._emptyRpcObject()
		rpc["proc"] = "GetProcessData"
		rpc["id"] = "4"
		rpc["params"] = {
			# dev_objects must be an array containing dicts with "key" and "channels"
			"devices" : dev_objects
		}
		return ScraperSolar._postRequest(rpc)

	def _postRequest(body={}):
		req = requests.post('http://%s:%d/rpc' % (sma_host, sma_port), data="RPC=%s" % json.dumps(body))
		return req.text

	def get_data(self):
		return []

if __name__ == '__main__':
	obj = ScraperSolar()
	from pprint import pprint
	pprint(obj.get_data())