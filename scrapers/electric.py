import requests, re, pytz, datetime
from commonssite.settings import veris_host, veris_port, veris_uname, veris_password
from commonssite.scrapers.xml_import import etree
from commonssite.server.data.models.electric import ChannelEntry, DeviceSummary

class ScraperElectric(object):
	"""A scraper class for gettind data from our veris system
	"""

	__devices = [2, 3, 4]
	#__datetime_fmt = '%Y-%m-%d %H:%M:%S' # format of incoming XML datetime string
	__channel_parser = re.compile(r'(Channel \#\d+)\s?(.*)')

	def __get_xml_string(self, channel):
		full_url = "http://%s:%d/setup/devicexml.cgi?ADDRESS=%d&TYPE=DATA" % (veris_host, veris_port, channel)
		req = requests.get(full_url, auth=(veris_uname, veris_password))
		return str(req.text)

	def __map_db_field(self, xml_name):
		# the name given by xml mapped to the field name in our DB object
		mapping = {
			'' : 'Current',
			'Max' : 'MaxCurrent',
			'Demand' : 'Demand',
			'Energy' : 'Energy',
			'Power' : 'Power',
			'Power Max' : 'MaxPower',
			'Power Demand' : 'PowerDemand',
			'Power Factor' : 'PowerFactor'
		}
		return mapping.get(xml_name)

	def __xml_to_db_entries(self, xml, set_time, set_panel):
		# TODO attrib['alarm'] and attrib['units']
		objects = {} # collection of under-construction model objects
		for pt in xml.findall('.//point'):
			n = pt.attrib['name']
			parse_name = self.__channel_parser.match(n)
			if parse_name:
				channel = parse_name.group(1)
				column = parse_name.group(2)
				val = pt.attrib['value']
				# get under-construction channel OR create new one
				obj = objects.get(channel, ChannelEntry(Time=set_time, Panel=set_panel))
				try:
					# all fields in this model should be float values
					obj.__dict__[self.__map_db_field(column)] = float(val)
				except:
					print "[ERROR] could not parse %s value as float: %s" % (column, val)
					obj.__dict__[self.__map_db_field(column)] = None
		return objects.values()

	def __xml_to_db_summary(self, xml, set_time, set_panel):
		# TODO parse xml, return DeviceSummary object
		pass

	def get_data(self):
		now = datetime.datetime.now()
		now = pytz.UTC.localize(now)
		retlist = []
		for d in self.__devices:
			status_string = self.__get_xml_string(d)
			xml_tree = etree.fromstring(status_string)
			# TODO better panel name
			retlist.extend(self.__xml_to_db_entries(xml_tree, now, 'Panel %d' % d))
			# TODO get device summary
		return retlist
