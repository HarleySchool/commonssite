import requests
import json
import time
import threading
import sys
from commonssite.settings import sma_host, sma_password, sma_port
# Thanks to these pdfs: 
# http://files.sma.de/dl/1348/NG_PAR-TB-en-22.pdf, 
# http://files.sma.de/dl/15330/SB3-6TL-21-Parameter-TI-en-10W.pdf
# for the mapping dict below
name_mapping_dict = {
	## OVERVIEW ##
	'GriPwr' : 'Total AC Power',
	'GriEgyTdy' : 'Total Energy Used Today',
	'GriEgyTot' : 'Total Energy Used',
	'Msg' : 'Message',
	## WEATHER ## 
	'ExlSolIrr' : 'Internal Solar Irradation',
	'IntSolIrr' : 'External Solar Irradation',
	'TmpAmb C' : 'Ambient Temprature',
	'TmpMdul C' : 'Module Temprature',
	'WindVel m/s' : 'Wind Velocity',
	## INVERTER ## 
	'A.Ms.Amp' : 'A DC Input',
	'A.Ms.Vol' : 'A DC Input',
	'A.Ms.Watt' : 'A DC Input',
	'A1.Ms.Amp' : 'A1 DC Input',
	'B.Ms.Amp' : 'B DC Input',
	'B.Ms.Vol' : 'B DC Input',
	'B.Ms.Watt' : 'B DC Input',
	'B1.Ms.Amp' : 'B1 DC Input',
	'E-Total' : 'Total Yield',
	'GM.TotS0Out' : 'S0-pulses grid feed-in counter',
	'GM.TotWhOut' : 'Feed in Reading',
	'GridMs.A.phsA' : 'Grid Phase 1 Current',
	'GridMs.A.phsB' : 'Grid Phase 2 Current',
	'GridMs.A.phsC' : 'Grid Phase 3 Current',
	'GridMs.Hz' : 'Grid Frequency',
	'GridMs.PhV.phsA' : 'Grid Phase 1 Voltage',
	'GridMs.PhV.phsB' : 'Grid Phase 2 Voltage',
	'GridMs.PhV.phsC' : 'Grid Phase 3 Voltage',
	'GridMs.TotPF' : 'Grid Displacement Power Factor',
	'GridMs.TotVA' : 'Grid Apparent Power',
	'GridMs.TotVAr' : 'Grid Reactive Power',
	'GridMs.VA.phsA' : 'Grid Phase 1 Apparent Power',
	'GridMs.VA.phsB' : 'Grid Phase 2 Apparent Power',
	'GridMs.VA.phsC' : 'Grid Phase 3 Apparent Power',
	'GridMs.VAr.phsA' : 'Grid Phase 1 Reactive Power',
	'GridMs.VAr.phsB' : 'Grid Phase 2 Reactive Power',
	'GridMs.VAr.phsC' : 'Grid Phase 3 Reactive Power',
	'GridMs.W.phsA' : 'Grid Phase 1 Power',
	'GridMs.W.phsB' : 'Grid Phase 2 Power',
	'GridMs.W.phsC' : 'Grid Phase 3 Power',
	'Inv.TmpLimStt' : 'Derating',

	'InvCtl.Stt' : 'Device Control Status',
	'Iso.FltA' : 'Residual current',
	'Mt.TotOpTmh' : 'Feed-in time',
	'Mt.TotTmh' : 'Operating time',
	'Op.EvtCntIstl' : 'Number of Installer-Relevant Events',
	'Op.EvtCntUsr' : 'Number of User-Relevant Events',
	'Op.EvtNo' : 'Current Event Number',
	'Op.GriSwCnt' : 'Number of Grid Connections',
	'Op.GriSwStt' : 'Grid relay/contactor',
	'Op.Health' : 'Operation Health',
	'Op.Prio' : 'Recomended Action',
	'Op.TmsRmg' : 'Waiting time until feed-in',
	'Pac' : 'Total AC Power',
	'PCM-DigInStt' : 'Status of digital inputs of power control module',
	'PlntCtl.Stt' : 'PV System Control Status',
	'Riso' : 'Insulation resistance'
}

class ScraperSMA(object):

	def __init__(self):
		self.__setdevs()

	# Take a standard name and return a human readable name
	def __mapdict(self, smaname):
		query = name_mapping_dict.get(smaname)
		if query == None:
			return smaname
		else:
			return query

	def __unitvalparse(self, val, unit):
		if val == '':
			return 'No Value'
		else:
			return val + ' ' + unit

	def __setdevs(self):
		devs = self.__doGetDevices()
		self.devlist = devs['result']['devices']
		# data = self.__doGetData(devlist)
		# self.actualdata = data['result']['devices']

	def __MD5Hash(self, s):
		import md5
		m = md5.new()
		m.update(s)
		return m.hexdigest()

	def __emptyDevObject(self):
		"""Creates a template JSON object (a python dict actually) according to
		the schema for a Device Object defined in section 6.1 of the RPC manual
		"""
		return {
			"key" : None,
			"name" : None,
			"channels" : None,
			"children" : None
		}

	def __emptyChannelObject(self):
		return {
			"meta" : None, # must be set
			"name" : None,
			"value" : None, # must be set
			"unit" : None,
			"min" : None,
			"max" : None,
			"options" : None
		}

	def __emptyRpcObject(self):
		"""Creates a template JSON object (a python dict actually) according to
		the schema for an RPC request defined in section 4.1 of the RPC manual
		"""
		return {
			'version' : '1.0',
			'proc' : '', # set by procedure functions
			'id' : '0',  # should probably set something smart
			'format' : 'JSON',
			'passwd' : self.__MD5Hash(sma_password),
			'params' : {}
		}

	def __doGetPlantOverview(self):
		rpc = self.__emptyRpcObject()
		rpc["proc"] = "GetPlantOverview"
		rpc["id"] = "4"
		return self.__postRequest(rpc)

	def __doGetDevices(self):
		rpc = self.__emptyRpcObject()
		rpc["proc"] = "GetDevices"
		rpc["id"] = "2"
		return self.__postRequest(rpc)

	def __doGetChannels(self, dev_obj):
		rpc = self.__emptyRpcObject()
		rpc["proc"] = "GetProcessDataChannels"
		rpc["id"] = "3"
		rpc["params"] = {
			"device" : dev_obj['key']
		}
		return self.__postRequest(rpc)

	def __doGetData(self):
		rpc = self.__emptyRpcObject()
		rpc["proc"] = "GetProcessData"
		rpc["id"] = "1"
		rpc["params"] = {
			# dev_objects must be an array containing dicts with "key" and "channels"
			"devices" : self.devlist
		}
		return self.__postRequest(rpc)

	def __postRequest(self, body={}):
		req = requests.post('http://%s:%d/solar/rpc' % (sma_host, sma_port), data="RPC=%s" % json.dumps(body))
		return req.json()

	def get_data(self):
		from pprint import pprint
		objects = []
		pprint(self.__doGetData())
		return objects

if __name__ == '__main__':
	scraper = ScraperSMA()
	scraper.get_data()
