import requests, re, pytz, datetime
from timeseries.scrapers import ScraperBase
from commonssite.settings import veris_host, veris_port, veris_uname, veris_password
from commonssite.scrapers.xml_import import etree
from commonssite.server.electric.models import CircuitEntry, DeviceSummary, Panel, Circuit, CalculatedStats

class ElectricServerInterface(object):
	"""The class in charge of handling the network interface with the veris server"""

	def get_xml_data(self, channel):
		full_url = "http://%s:%d/setup/devicexml.cgi?ADDRESS=%d&TYPE=DATA" % (veris_host, veris_port, channel)
		req = requests.get(full_url, auth=(veris_uname, veris_password), timeout=5.0)
		return etree.fromstring(str(req.text))

	
class VerisScraperBase(ScraperBase):
	"""A scraper class for gettind data from our veris system
	"""

	def __init__(self, model, registry_instance):
		super(VerisScraperBase, self).__init__(model, registry_instance)

		self.devices = [2, 3, 4]
		#__datetime_fmt = '%Y-%m-%d %H:%M:%S' # format of incoming XML datetime string
		self.channel_parser = re.compile(r'(Channel \#\d+)\s?(.*)')

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
				channel_hash_num = parse_name.group(1) # this comes in in the format "Channel #1" to "Channel #42"
				column = parse_name.group(2)
				try:
					channel_num = int(channel_hash_num[channel_hash_num.find("#")+1:])
					circuit_obj = Circuit.objects.get(panel=set_panel, veris_id=channel_num)
				except:
					"[ERROR] ScraperCircuits encountered an unknown channel:", channel_hash_num, "on", set_panel
					continue
				val = pt.attrib['value']
				# get under-construction channel OR create new one
				obj = objects.get(channel_hash_num, CircuitEntry(Time=set_time, Circuit=circuit_obj))
				# all fields in this model should be float values (if not, caught by get_data and status_format_error() is called)
				obj.__dict__[self.map_db_field(column)] = float(val)
			objects[channel_hash_num] = obj
		return objects.values()

	def get_data(self):
		retlist = []
		try:
			esi = ElectricServerInterface()
			now = pytz.UTC.localize(datetime.datetime.utcnow())
			for d in self.devices:
				xml_tree = esi.get_xml_data(d)
				try:
					panel_obj = Panel.objects.get(veris_id=d)
				except:
					print "[ERROR] ScraperCircuits could not find Panel", d
				retlist.extend(self.__xml_to_db_entries(xml=xml_tree, set_time=now, set_panel=panel_obj))
			self.status_ok()
		except requests.exceptions.RequestException:
			self.status_comm_error()
		except Exception:
			# any other exception implies that the transaction took place but we weren't able to parse it
			self.status_format_error()
		return retlist

class ScraperPowerSummary(VerisScraperBase):

	def __init__(self, model, registry_instance):
		super(ScraperPowerSummary, self).__init__(model, registry_instance)

	def __xml_to_db_summary(self, xml, set_time, set_panel):
		summary_obj = DeviceSummary(Time=set_time, Panel=set_panel)
		for pt in xml.findall('.//point'):
			n = pt.attrib['name']
			parse_name = self.channel_parser.match(n)
			if not parse_name: # anything that doesn't match the 'Channel #1' - 'Channel #42' pattern is part of summary data
				column = self.map_db_field(n)
				val = pt.attrib['value']
				summary_obj.__dict__[column] = float(val)
		return [summary_obj]

	def get_data(self):
		retlist = []
		try:
			esi = ElectricServerInterface()
			now = pytz.UTC.localize(datetime.datetime.utcnow())
			for d in self.devices:
				xml_tree = esi.get_xml_data(d)
				try:
					panel_obj = Panel.objects.get(veris_id=d)
				except:
					print "[ERROR] ScraperPowerSummary could not find Panel", d
				retlist.extend(self.__xml_to_db_summary(xml=xml_tree, set_time=now, set_panel=panel_obj))
			self.status_ok()
		except requests.exceptions.RequestException:
			self.status_comm_error()
		except Exception:
			self.status_format_error()
		return retlist

if __name__ == '__main__':
	from timeseries.models import ModelRegistry
	from pprint import pprint
	
	sc  = ScraperCircuits(CircuitEntry, ModelRegistry.objects.get(short_name="Circuits"))
	sps = ScraperPowerSummary(DeviceSummary, ModelRegistry.objects.get(short_name="Electric Overview"))

	pprint(sc.get_data())
	pprint(sps.get_data())

class ScraperCalculatedStats(ScraperBase):

	def get_data(self):
		"""custom net- and gross-calculations based on latest circuits scrape
		"""
		latest_circuits = CircuitEntry.objects.filter(Time=CircuitEntry.latest(temporary=True))
		if len(latest_circuits) == 0: return []

		gross_power_used = 0.0
		gross_energy_used = 0.0
		gross_power_produced = 0.0
		gross_energy_produced = 0.0

		# see mysql database or electric/fixtures/initial_data.json
		# these correspond to panel #4 channels #8, #10, #12
		solar_circuit_ids = [92, 94, 96]

		for measurement in latest_circuits:
			if measurement.Circuit.id in solar_circuit_ids:
				gross_power_produced += abs(measurement.Power)
				gross_energy_produced += abs(measurement.Energy)
			else:
				gross_power_used += abs(measurement.Power)
				gross_energy_used += abs(measurement.Energy)

		net_power = gross_power_used - gross_power_produced
		net_energy = gross_energy_used - gross_energy_produced

		return [CalculatedStats(Time=latest_circuits[0].Time,
			NetPower=net_power,
			NetEnergy=net_energy,
			GrossPowerUsed=gross_power_used,
			GrossEnergyUsed=gross_energy_used,
			GrossPowerProduced=gross_power_produced,
			GrossEnergyProduced=gross_energy_produced)]
