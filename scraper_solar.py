import requests, json
from settings import sma_host, sma_port, sma_password

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

def MD5Hash(s):
	import md5
	m = md5.new()
	m.update(s)
	return m.hexdigest()

def emptyDevObject():
	"""Creates a template JSON object (a python dict actually) according to
	the schema for a Device Object defined in section 6.1 of the RPC manual
	"""
	return {
		"key" : None,
		"name" : None,
		"channels" : None,
		"children" : None
	}

def emptyChannelObject():
	return {
		"meta" : None, # must be set
		"name" : None,
		"value" : None, # must be set
		"unit" : None,
		"min" : None,
		"max" : None,
		"options" : None
	}

def emptyRpcObject():
	"""Creates a template JSON object (a python dict actually) according to
	the schema for an RPC request defined in section 4.1 of the RPC manual
	"""
	return {
		'version' : '1.0',
		'proc' : '', # set by procedure functions
		'id' : '0',  # should probably set something smart
		'format' : 'JSON',
		'passwd' : MD5Hash(sma_password),
		'params' : {}
	}

def doGetPlantOverview():
	rpc = emptyRpcObject()
	rpc["proc"] = "GetPlantOverview"
	rpc["id"] = "1"
	return postRequest(rpc)

def doGetDevices():
	rpc = emptyRpcObject()
	rpc["proc"] = "GetDevices"
	rpc["id"] = "2"
	return postRequest(rpc)

def doGetChannels(dev_obj):
	rpc = emptyRpcObject()
	rpc["proc"] = "GetProcessDataChannels"
	rpc["id"] = "3"
	rpc["params"] = {
		"device" : dev_obj['key']
	}
	return postRequest(rpc)

def doGetData(dev_objects):
	rpc = emptyRpcObject()
	rpc["proc"] = "GetProcessData"
	rpc["id"] = "4"
	rpc["params"] = {
		# dev_objects must be an array containing dicts with "key" and "channels"
		"devices" : dev_objects
	}
	return postRequest(rpc)

def postRequest(body={}):
	req = requests.post('http://%s:%d/rpc' % (sma_host, sma_port), data="RPC=%s" % json.dumps(body))
	return req.text

if __name__ == '__main__':
	from pprint import pprint
	pprint(json.loads(doGetPlantOverview()))
	pprint(json.loads(doGetDevices()))
	pprint(json.loads(doGetChannels(devices['power'])))
	pprint(json.loads(doGetData([devices['power']])))
	pprint(json.loads(doGetChannels(devices['weather'])))
	pprint(json.loads(doGetData([devices['weather']])))