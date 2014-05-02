import requests
import json
import datetime
import pytz
from timeseries.scrapers import ScraperBase
from commonssite.settings import sma_host, sma_password, sma_port
from commonssite.server.solar.models import SMAWeather, SMAPanels, SMAOverview


devices = {
	'weather' : {
		'key' : 'SENS0700:26877',
		'name' : 'SMA Weather Sensor',
		'channels' : 'null',
		'children' : 'null'
	},
	'power' : {
		'key' : 'WRHV5K84:191201464',
		'name' : 'SMA Solar Data',
		'channels' : 'null',
		'children' : 'null'
	}
}

class SMAServerInterface(object):

	def __init__(self):
		self.__setdevs()

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
		import hashlib
		m = hashlib.md5()
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

	def __postRequest(self, body={}):
		req = requests.post('http://%s:%d/solar/rpc' % (sma_host, sma_port), data="RPC=%s" % json.dumps(body))
		return req.json()

	def doGetData(self):
		rpc = self.__emptyRpcObject()
		rpc["proc"] = "GetProcessData"
		rpc["id"] = "1"
		rpc["params"] = {
			# dev_objects must be an array containing dicts with "key" and "channels"
			"devices" : self.devlist
		}
		return self.__postRequest(rpc)

	def doGetPlantOverview(self):
		rpc = self.__emptyRpcObject()
		rpc["proc"] = "GetPlantOverview"
		rpc["id"] = "4"
		return self.__postRequest(rpc)

class SMAScraperBase(ScraperBase):


	def __init__(self, model, registry_instance):
		super(SMAScraperBase, self).__init__(model, registry_instance)

	# Thanks to these pdfs: 
	# http://files.sma.de/dl/1348/NG_PAR-TB-en-22.pdf, 
	# http://files.sma.de/dl/15330/SB3-6TL-21-Parameter-TI-en-10W.pdf
	# for the mapping dict below
	name_mapping_dict = {
		'overview' : {
			'GriPwr' : 'TotalACPower',
			'GriEgyTdy' : 'TotalEnergyToday',
			'GriEgyTot' : 'TotalEnergy',
			'Msg' : 'Message',
		},
		'weather' : {
			'ExlSolIrr' : 'InternalSolarIrradation',
			'IntSolIrr' : 'ExternalSolarIrradation',
			'TmpAmb C' : 'AmbientTemprature',
			'TmpMdul C' : 'ModuleTemprature',
			'WindVel m/s' : 'WindVelocity',
		},
		'panels' : { 
			'A.Ms.Amp' : 'A_DC_Current',
			'A.Ms.Vol' : 'A_DC_Voltage',
			'A.Ms.Watt' : 'A_DC_Power',
			'A1.Ms.Amp' : 'A1_DC_Current',
			'B.Ms.Amp' : 'B_DC_Current',
			'B.Ms.Vol' : 'B_DC_Voltage',
			'B.Ms.Watt' : 'B_DC_Power',
			'B1.Ms.Amp' : 'B1_DC_Current',
			'GridMs.A.phsA' : 'GridPhase1Current',
			'GridMs.A.phsB' : 'GridPhase2Current',
			'GridMs.A.phsC' : 'GridPhase3Current',
			'GridMs.Hz' : 'GridFrequency',
			'GridMs.PhV.phsA' : 'GridPhase1Voltage',
			'GridMs.PhV.phsB' : 'GridPhase2Voltage',
			'GridMs.PhV.phsC' : 'GridPhase3Voltage',
			'GridMs.TotPF' : 'GridDisplacementPowerFactor',
			'GridMs.TotVA' : 'GridApparentPower',
			'GridMs.TotVAr' : 'GridReactivePower',
			'GridMs.VA.phsA' : 'GridPhase1ApparentPower',
			'GridMs.VA.phsB' : 'GridPhase2ApparentPower',
			'GridMs.VA.phsC' : 'GridPhase3ApparentPower',
			'GridMs.VAr.phsA' : 'GridPhase1ReactivePower',
			'GridMs.VAr.phsB' : 'GridPhase2ReactivePower',
			'GridMs.VAr.phsC' : 'GridPhase3ReactivePower',
			'GridMs.W.phsA' : 'GridPhase1Power',
			'GridMs.W.phsB' : 'GridPhase2Power',
			'GridMs.W.phsC' : 'GridPhase3Power',
			'Inv.TmpLimStt' : 'Derating',
			'InvCtl.Stt' :'DeviceControlStatus',
			'Op.Health' : 'OperationHealth',
			'E-Total' : 'TotalYield',
			'Iso.FltA' : 'ResidualCurrent',
			'Mt.TotOpTmh' : 'FeedInTime',
			'Mt.TotTmh' : 'OperatingTime',

			# 'Op.EvtCntIstl' : 
			# 'Op.EvtCntUsr' : 
			# 'Op.EvtNo' : 
			# 'Op.GriSwCnt' : 
			# 'Op.GriSwStt' : 
			# 'Op.Prio' : 
			# 'Op.TmsRmg' : 
			# 'Pac' : 
			# 'PCM-DigInStt' : 
			# 'PlntCtl.Stt' : 
			# 'Riso' : 
			# 'GM.TotS0Out' : 
			# 'GM.TotWhOut' : 
		}
	}

	# Take a standard name and return a human readable name (default to the standard name)
	def map_dict(self, dname, smaname):
		return SMAScraperBase.name_mapping_dict[dname].get(smaname, smaname)

	def supports_sma_field(self, dname, smaname):
		return smaname in SMAScraperBase.name_mapping_dict.get(dname, {})

class ScraperSolarPanels(SMAScraperBase):

	def __init__(self, model, registry_instance):
		super(ScraperSolarPanels, self).__init__(model, registry_instance)
	
	def get_data(self):
		# TODO convert given units to default units
		ssi = SMAServerInterface()

		try:
			now = pytz.UTC.localize(datetime.datetime.utcnow())
			objects = []
			# GET DEVICE DATA
			data_dict = ssi.doGetData()
			if 'id' in data_dict and int(data_dict['id']) == 1: # part of the SMA RPC protocol
				for dev_dict in data_dict['result']['devices']:
					if dev_dict.get('key') == devices['power']['key']:
						# PARSE PANELS
						channel_info = dev_dict['channels']
						kwargs = {}
						for field in channel_info:
							nm = field['name']
							try:
								val = float(field['value'])
							except:
								val = field['value']
							if self.supports_sma_field('panels', nm):
								kwargs[self.map_dict('panels', nm)] = val
						panel_obj = SMAPanels(Time=now, **kwargs)
						objects.append(panel_obj)
			self.status_ok()
		except requests.exceptions.ConnectionError:
			self.status_down()
		except Exception:
			# any other exception implies that the transaction took place but we weren't able to parse it
			self.status_comm_error()
		return objects

class ScraperSolarWeather(SMAScraperBase):

	def __init__(self, model, registry_instance):
		super(ScraperSolarWeather, self).__init__(model, registry_instance)

	def get_data(self):
		# TODO convert given units to default units
		ssi = SMAServerInterface()

		try:
			now = pytz.UTC.localize(datetime.datetime.utcnow())
			objects = []
			# GET DEVICE DATA
			data_dict = ssi.doGetData()
			if 'id' in data_dict and int(data_dict['id']) == 1:
				for dev_dict in data_dict['result']['devices']:
					if dev_dict.get('key') == devices['weather']['key']:
						# PARSE WEATHER
						weather_info = dev_dict['channels']
						kwargs = {}
						for field in weather_info:
						 	nm = field['name']
						 	try:
						 		val = float(field['value'])
						 	except:
						 		val = field['value']
						 	if self.supports_sma_field('weather', nm):
							 	kwargs[self.map_dict('weather', nm)] = val
						weather_obj = SMAWeather(Time=now, **kwargs)
						objects.append(weather_obj)
			self.status_ok()
		except requests.exceptions.ConnectionError:
			self.status_down()
		except Exception:
			# any other exception implies that the transaction took place but we weren't able to parse it
			self.status_comm_error()
		return objects

class ScraperSolarOverview(SMAScraperBase):

	def __init__(self, model, registry_instance):
		super(ScraperSolarOverview, self).__init__(model, registry_instance)

	def get_data(self):
		# TODO convert given units to default units
		ssi = SMAServerInterface()

		try:
			now = pytz.UTC.localize(datetime.datetime.utcnow())
			objects = []
			# GET OVERVIEW DATA
			over_dict = ssi.doGetPlantOverview()
			if 'id' in over_dict and int(over_dict['id']) == 4:
				overview_info = over_dict['result']['overview']
				kwargs = {}
				for field in overview_info:
					nm = field['name']
					try:
						val = float(field['value'])
					except:
						val = field['value']
					if self.supports_sma_field('overview', nm):
						kwargs[self.map_dict('overview', nm)] = val
				overview_obj = SMAOverview(Time=now, **kwargs)
				objects.append(overview_obj)
			self.status_ok()
		except requests.exceptions.ConnectionError:
			self.status_down()
		except Exception:
			# any other exception implies that the transaction took place but we weren't able to parse it
			self.status_comm_error()
		return objects
