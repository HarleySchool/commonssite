import time, string, requests
from settings import hvac_host, hvac_port
from pprint import pprint
from xml_import import etree
from scraper_template import ScraperTemplate

# bulk-parsing lookup tables
bulk_lookup_table = {
	'Drive' : {
		0: 'OFF',
		1: 'ON',
		2: 'TestRun',
		4: 'ON',
		5: 'ON'
	},
	'Mode' : {
		0: "Fan",
		1: "Cool",
		2: "Heat",
		3: "Dry",
		4: "Auto",
		5: "BAHP",
		6: "AUTOCOOL",
		7: "AUTOHEAT",
		8: "VENTILATE",
		9: "PANECOOL",
		10: "PANEHEAT",
		11: "OUTCOOL",
		12: "DEFLOST",
		128: "HEATRECOVERY",
		129: "BYPASS",
		130: "LC_AUTO"
	},
	'AirDirection': {
		0: 'Swing',
		1: 'Vertical',
		2: 'Mid-Vertical',# TODO check mid values
		3: 'Mid-Horizontal',
		4: 'Horizontal',
		5: 'Mid',
		6: 'Auto'
	},
	'FanSpeed' : {
		0: 'Low', 
		1: 'Mid-Low', # TODO check mid values
		2: 'Mid-High',
		3: 'High',
		6: 'Auto'
	},
	'Ventilation' : {
		0: 'OFF',
		1: 'LOW',
		2: 'HIGH',
		3: 'NONE'
	},
	'Model' : {
		1 : 'FU',
		2 : 'LC',
		3 : 'OC',
		4 : 'BC',
		5 : 'IU',
		6 : 'OS',
		18 : 'TU',
		7 : 'SC',
		8 : 'GW',
		9 : 'TR',
		10 : 'AN',
		11 : 'KA',
		12 : 'MA',
		13 : 'IDC',
		14 : 'MC',
		15 : 'CDC',
		16 : 'VDC',
		31 : 'IC',
		32 : 'DDC',
		33 : 'RC',
		34 : 'KIC',
		35 : 'AIC',
		36 : 'GR',
		37 : 'OCi',
		38 : 'BS',
		39 : 'SC',
		40 : 'IC',
		41 : 'ME',
		42 : 'CR',
		43 : 'SR',
		44 : 'ST',
		50 : 'DC',
		51 : 'MCt',
		52 : 'MCp',
		96 : 'NOUSE',
		97 : 'TMP',
		98 : '??',
		99 : 'NONE'
	},
	'FanSpeedSW' : {
		0 : '2-Stage',
		1 : '4-Stage',
		2 : 'None',
		3 : '3-Stage'
	},
	'IcKind' : {
		0 : 'Cool',
		1 : 'Normal'
	},
	############
	# GENERICS #
	############
	'resetable' : {
		0 : 'OFF',
		1 : 'ON', 
		2 : 'RESET'
	},
	'onoff' : {
		0 : 'OFF',
		1 : 'ON'
	}, 
	'enable' : {
		0 : 'DISABLED',
		1 : 'ENABLED'
	}
}

# bulk-parsing types (used for conversions)
# note that changing the type will not affect how these are _parsed_, but how
# the parsed values are interpreted
bulk_types = {
	'Drive': 'text',
	'Mode': 'text',
	'SetTemp': 'temp',
	'InletTemp': 'temp',
	'AirDirection': 'text',
	'FanSpeed': 'text',  
	'RemoteControl': 'enable',
	'DriveItem': 'onoff',
	'ModeItem': 'onoff',
	'SetTempItem' : 'onoff',
	'FilterItem' : 'onoff',
	'Ventilation' : 'text',
	'FilterSign' : 'resetable',
	'ErrorSign' : 'resetable',
	'Model' : 'text',
	'ModeStatus' : 'enable',
	'MidTemp' : 'enable',
	'ControlValue' : 'text', # this one made no sense
	'Timer' : 'text',
	'IcKind' : 'text',
	'AutoModeSW' : 'enable',
	'DryModeSW' : 'enable',
	'FanSpeedSW' : 'text',
	'AirDirectionSW' : 'enable',
	'SwingSW' : 'enable',
	'VentilationSW' : 'enable',
	'BypassSW' : 'enable',
	'LcAutoSW' : 'enable',
	'HeatRecoverySW' : 'enable',
	'CoolMin' : 'temp',
	'HeatMax' : 'temp',
	'CoolMax' : 'temp',
	'HeatMin' : 'temp',
	'AutoMin' : 'temp',
	'AutoMax' : 'temp',
	'TurnOff' : 'onoff',
	'TempLimit' : 'enable',
	'TempDetail' : 'enable',
	'FanModeSW' : 'enable',
	'AirStageSW' : 'enable',
	'AirAutoSW' : 'enable',
	'FanAutoSW' : 'enable'
}

unit_descriptions = {
	'degC' : 'floating point degrees celcius',
	'degF' : 'floating point degrees farenheit',
	'text' : 'some arbitrary string',
	'bool' : 'boolean True or False',
	'upper' : 'upper-case string',
	'lower' : 'lower-case string',
	'anycase' : 'mixed-case string (only convert *from* anycase *to* upper or lower'
}

# the default units returned by the lookup table and by parsing functions
# note that this dict describes how those work, it does not alter them.
# (that is, setting 'text' to 'upper' will not force all text to output in upper-case..
# that is the job of the user's 'units' dict)
default_units = {
	'temp': 'degC',
	'onoff': 'upper',
	'enable': 'upper',
	'resetable': 'upper',
	'text': 'anycase'
}

# a dict of converting from one unit type to another
conversions = {
	'degC' : {
		'degF': (lambda t: t*1.8+32.0)
	},
	'degF' : {
		'degC': (lambda t: (t-32.0) / 1.8)
	},
	'anycase' : {
		'lower' : (lambda s: string.lower(s)),
		'upper' : (lambda s: string.upper(s)),
	},
	'upper' : {
		'lower' : (lambda s: string.lower(s)),
		'anycase' : (lambda s: s),
	},
	'lower' : {
		'anycase' : (lambda s: s),
		'upper' : (lambda s: string.upper(s)),
	}
}

class ScraperHvac(ScraperTemplate):

	def __init__(self):
		ScraperTemplate.__init__(self, "hvac")

	def parse_bulk(self, bulk, selection=[], units={}):
		"""given bulk hex data describing a VRF group, this function returns a dict
		of readable and sensible values"""
		data = {}

		# helper functions for block_parsers

		def blocks(byte_index, len):
			lo = 2*byte_index
			hi = lo+2*len
			return bulk[lo:hi]

		def nibblex(byte_index, offset):
			return int(bulk[2*byte_index + offset], 16)

		def blockx(byte_index, len):
			return int(blocks(byte_index, len), 16)

		def blocki(byte_index, len):
			return int(blocks(byte_index, len), 10)

		# a data structure mapping from data name to parse function
		# with thanks to the documentation from https://gitorious.org/g50a-commander
		block_parsers = {
			'Drive'			: (lambda b: bulk_lookup_table['Drive'].get(blockx(1, 1))),
			'Mode'			: (lambda b: bulk_lookup_table['Mode'].get(blockx(2, 1))),
			'SetTemp'		: (lambda b: float(blockx(3,1)) + 0.1 * float(blockx(4,1))),
			'InletTemp'		: (lambda b: float(blockx(5,2)) * 0.1),
			'AirDirection'	: (lambda b: bulk_lookup_table['AirDirection'].get(blockx(7,1))),
			'FanSpeed'		: (lambda b: bulk_lookup_table['FanSpeed'].get(blockx(8,1))),
			'RemoteControl'	: (lambda b: bulk_lookup_table['enable'].get(1-blockx(9,1))), # note the 1-block().. special case 0 enabled 1 disable
			'DriveItem'		: (lambda b: bulk_lookup_table['onoff'].get(blockx(10,1))),
			'ModeItem'		: (lambda b: bulk_lookup_table['onoff'].get(blockx(11,1))),
			'SetTempItem'	: (lambda b: bulk_lookup_table['onoff'].get(blockx(12,1))),
			'FilterItem'	: (lambda b: bulk_lookup_table['onoff'].get(blockx(13,1))),
			'Ventilation'	: (lambda b: bulk_lookup_table['Ventilation'].get(blockx(14,1))),
			'FilterSign'	: (lambda b: bulk_lookup_table['resetable'].get(blockx(15,1))),
			'ErrorSign'		: (lambda b: bulk_lookup_table['resetable'].get(blockx(16,1))),
			'Model' 		: (lambda b: bulk_lookup_table['Model'].get(blockx(17,1))),
			'ModeStatus' 	: (lambda b: bulk_lookup_table['enable'].get(blockx(18,1))),
			'MidTemp'		: (lambda b: bulk_lookup_table['enable'].get(blockx(19,1))),
			'ControlValue'	: (lambda b: '0x%s (Unknown)' % blocks(20,1)), # this one is a mystery. just print the hex
			'Timer'			: (lambda b: bulk_lookup_table['onoff'].get(blockx(21,1))),
			'IcKind'		: (lambda b: bulk_lookup_table['IcKind'].get(blockx(22,1))),
			'AutoModeSW'	: (lambda b: bulk_lookup_table['enable'].get(blockx(23,1))),
			'DryModeSW'		: (lambda b: bulk_lookup_table['enable'].get(blockx(24,1))),
			'FanSpeedSW'	: (lambda b: bulk_lookup_table['FanSpeedSW'].get(blockx(25,1))),
			'AirDirectionSW': (lambda b: bulk_lookup_table['enable'].get(blockx(26,1))),
			'SwingSW'		: (lambda b: bulk_lookup_table['enable'].get(blockx(27,1))),
			'VentilationSW'	: (lambda b: bulk_lookup_table['enable'].get(blockx(28,1))),
			'BypassSW'		: (lambda b: bulk_lookup_table['enable'].get(blockx(29,1))),
			'LcAutoSW'		: (lambda b: bulk_lookup_table['enable'].get(blockx(30,1))),
			'HeatRecoverySW': (lambda b: bulk_lookup_table['enable'].get(blockx(31,1))),
			'CoolMin'		: (lambda b: float(blocki(32, 1)) + 0.1 * float(nibblex(38, 0))),
			'HeatMax'		: (lambda b: float(blocki(33, 1)) + 0.1 * float(nibblex(38, 1))),
			'CoolMax'		: (lambda b: float(blocki(34, 1)) + 0.1 * float(nibblex(39, 0))),
			'HeatMin'		: (lambda b: float(blocki(35, 1)) + 0.1 * float(nibblex(39, 1))),
			'AutoMin'		: (lambda b: float(blocki(36, 1)) + 0.1 * float(nibblex(40, 0))),
			'AutoMax'		: (lambda b: float(blocki(37, 1)) + 0.1 * float(nibblex(40, 1))),
			'TurnOff'		: (lambda b: bulk_lookup_table['onoff'].get(blockx(41,1))),
			'TempLimit'		: (lambda b: bulk_lookup_table['enable'].get(blockx(42,1))),
			'TempDetail'	: (lambda b: bulk_lookup_table['enable'].get(blockx(43,1))),
			'FanModeSW'		: (lambda b: bulk_lookup_table['enable'].get(blockx(44,1))),
			'AirStageSW'	: (lambda b: bulk_lookup_table['enable'].get(blockx(45,1))),
			'AirAutoSW'		: (lambda b: bulk_lookup_table['enable'].get(blockx(46,1))),
			'FanAutoSW'		: (lambda b: bulk_lookup_table['enable'].get(blockx(47,1)))
		}

		# a helper function for converting a given value from the default units to the 'usr' units
		def unit_convert(val, default, usr):
			if default is None:
				print "# Default unit is none"
			elif usr is None:
				pass
			elif default != usr:
				if default in conversions and usr in conversions[default]:
					func = conversions[default][usr]
					try:
						val = func(val)
					except:
						print "Cannot convert", val, "from", default, "to", usr
				elif default in conversions:
					print "Cannot convert from", default, "to", usr
					print "\tValid options are:\n%s" % ("".join(["\t%s\n" % s for s in conversions[default].keys()]))
			return val

		# Here is where parsing the 'Bulk' text actually happens
		# ... loop over name:parser_func pairs
		for name, parser_func in block_parsers.iteritems():
			# selection as [] means "all values"
			# ..only add selected values to the data dict
			if selection == [] or name in selection:
				# parse with defaults
				value = parser_func(bulk)
				# handle unit conversion
				typename = bulk_types.get(name)
				# special case: temp is 'None' if zero
				if typename == 'temp' and value == 0.0:
					value = None
				else:
					default = default_units.get(typename)
					#print name, typename, default
					convert = units.get(typename)
					value = unit_convert(value, default, convert)
				# store value
				data[name] = value
		return data

	def get_xml_string(self, groups=[]):
		mnet_strings = '\n'.join(['<Mnet Group="%d" Bulk="*" EnergyControl="*" SetbackControl="*" ScheduleAvail="*" />' % g for g in groups])
		body = '<?xml version="1.0" encoding="UTF-8"?><Packet><Command>getRequest</Command><DatabaseManager>%s</DatabaseManager></Packet>' % mnet_strings
		full_url = 'http://%s:%d/servlet/MIMEReceiveServlet' % (hvac_host, hvac_port)
		headers = {
			'Content-type': 'text/xml',
			'Accept': 'text/html, image/gif, image/jpeg, *;'
		}
		req = requests.post(full_url, data=body, headers=headers)
		return str(req.text)

	def status(self, groups=[], values=[], units={}):
		# parse as xml 'element tree'
		r = self.get_xml_string(groups)
		xml_response = etree.fromstring(r)
		# get all relevant (Mnet) tags
		xml_group_objs = xml_response.findall(".//Mnet")
		# build result dict
		group_status = {}
		for grp in xml_group_objs:
			group_id = int(grp.get("Group"))
			group_status[group_id] = self.parse_bulk(grp.get("Bulk"), selection=values, units=units)
		return group_status

	def get_data(self):
		pass

if __name__ == '__main__':
	UNITS = {
		'temp': 'degF', 
		'text': 'upper'
	}

	scraper = ScraperHvac()

	from pprint import pprint
	pprint(scraper.status([i+1 for i in range(15)], COLUMNS, UNITS))
