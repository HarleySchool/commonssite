import requests, re, pytz, datetime
from timeseries.scrapers import ScraperBase
from commonssite.settings import veris_host, veris_port, veris_uname, veris_password
from commonssite.scrapers.xml_import import etree
from commonssite.server.electric.models import ChannelEntry, DeviceSummary

class ElectricServerInterface(object):
	"""The class in charge of handling the network interface with the veris server"""

	def get_xml_data(self, channel):
		full_url = "http://%s:%d/setup/devicexml.cgi?ADDRESS=%d&TYPE=DATA" % (veris_host, veris_port, channel)
		req = requests.get(full_url, auth=(veris_uname, veris_password))
		return etree.fromstring(str(req.text))

	
class VerisScraperBase(ScraperBase):
	"""A scraper class for gettind data from our veris system
	"""

	def __init__(self, model, registry_instance):
		super(VerisScraperBase, self).__init__(model, registry_instance)

	devices = [2, 3, 4]
	#__datetime_fmt = '%Y-%m-%d %H:%M:%S' # format of incoming XML datetime string
	channel_parser = re.compile(r'(Channel \#\d+)\s?(.*)')

	def map_db_field(self, xml_name):
		# the name given by xml mapped to the field name in our DB object
		mapping = {
			## SINGLE CHANNEL ##
			'' : 'Current',
			'Max' : 'MaxCurrent',
			'Demand' : 'Demand',
			'Energy' : 'Energy',
			'Power' : 'Power',
			'Power Max' : 'MaxPower',
			'Power Demand' : 'PowerDemand',
			'Power Factor' : 'PowerFactor',
			## SUMMARY VALUES ##
			'Frequency' : 'Frequency',
			'Volts L-N 3ph Ave' : 'LineNeutral',
			'Volts L-L 3ph Ave' : 'LineLine',
			'Volts A-N' : 'AToNeutral',
			'Volts B-N' : 'BToNeutral',
			'Volts C-N' : 'CToNeutral',
			'Volts A-B' : 'AToB',
			'Volts B-C' : 'BToC',
			'Volts C-A' : 'CToA',
			'3ph kWh' : 'TotalEnergy',
			'3ph Total kW' : 'TotalPower',
			'3ph Total PF' : 'TotalPowerFactor',
			'3ph Ave Current' : 'AverageCurrent3Phase',
			'kW Phase 1' : 'Phase1Power',
			'kW Phase 2' : 'Phase2Power',
			'kW Phase 3' : 'Phase3Power',
			'PF Phase 1' : 'Phase1PowerFactor',
			'PF Phase 2' : 'Phase2PowerFactor',
			'PF Phase 3' : 'Phase3PowerFactor',
			'Current Phase 1' : 'Phase1Current',
			'Current Phase 2' : 'Phase2Current',
			'Current Phase 3' : 'Phase3Current',
			'Current Phase 4' : 'PhaseNeutralCurrent',
			'Current Demand Phase 1' : 'Phase1Demand',
			'Current Demand Phase 2' : 'Phase2Demand',
			'Current Demand Phase 3' : 'Phase3Demand',
			'Current Demand Phase 4' : 'PhaseNeutralDemand',
			'Max Current Demand Phase 1' : 'Phase1MaxDemand',
			'Max Current Demand Phase 2' : 'Phase2MaxDemand',
			'Max Current Demand Phase 3' : 'Phase3MaxDemand',
			'Max Current Demand Phase 4' : 'PhaseNeutralMaxDemand',
			'3ph Present KW Total Demand' : 'Demand',
			'3ph Max KW Total Demand' : 'MaxDemand',
			'Max Current Phase 1' : 'Phase1MaxCurrent',
			'Max Current Phase 2' : 'Phase2MaxCurrent',
			'Max Current Phase 3' : 'Phase3MaxCurrent',
			'Max Current Phase 4' : 'PhaseNeutralMaxCurrent',
			'3ph Max KW Total' : 'MaxPower'
		}
		return mapping.get(xml_name)


class ScraperCircuits(VerisScraperBase):

	def __init__(self, model, registry_instance):
		super(ScraperCircuits, self).__init__(model, registry_instance)

	def __xml_to_db_entries(self, xml, set_time, set_panel):
		# TODO attrib['alarm'] and attrib['units']
		objects = {} # collection of under-construction model objects
		for pt in xml.findall('.//point'):
			n = pt.attrib['name']
			parse_name = self.channel_parser.match(n)
			if parse_name:
				channel = parse_name.group(1)
				column = parse_name.group(2)
				val = pt.attrib['value']
				# get under-construction channel OR create new one
				obj = objects.get(channel, ChannelEntry(Time=set_time, Panel=set_panel, Channel=channel))
				try:
					# all fields in this model should be float values
					obj.__dict__[self.map_db_field(column)] = float(val)
				except:
					print "[ERROR] could not parse %s value as float: %s" % (column, val)
					obj.__dict__[self.map_db_field(column)] = None
			objects[channel] = obj
		return objects.values()

	def get_data(self):
		esi = ElectricServerInterface()
		now = pytz.UTC.localize(datetime.datetime.utcnow())
		retlist = []
		for d in self.devices:
			xml_tree = esi.get_xml_data(d)
			# TODO better panel name
			retlist.extend(self.__xml_to_db_entries(xml_tree, now, 'Panel %d' % d))
		return retlist

class ScraperPowerSummary(VerisScraperBase):

	def __init__(self, model, registry_instance):
		super(ScraperPowerSummary, self).__init__(model, registry_instance)

	def __xml_to_db_summary(self, xml, set_time, set_panel):
		summary_obj = DeviceSummary(Time=set_time, Panel=set_panel)
		for pt in xml.findall('.//point'):
			n = pt.attrib['name']
			parse_name = self.channel_parser.match(n)
			if not parse_name:
				column = self.map_db_field(n)
				val = pt.attrib['value']
				try:
					summary_obj.__dict__[column] = float(val)
				except:
					print "[ERROR] could not parse %s value as float: %s" % (column, val)
					summary_obj.__dict__[self.map_db_field(column)] = None
		return [summary_obj]

	def get_data(self):
		esi = ElectricServerInterface()
		now = pytz.UTC.localize(datetime.datetime.utcnow())
		retlist = []
		for d in self.devices:
			xml_tree = esi.get_xml_data(d)
			# TODO better panel name
			retlist.extend(self.__xml_to_db_summary(xml_tree, now, 'Panel %d' % d))
		return retlist
