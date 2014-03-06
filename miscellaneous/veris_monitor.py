# veris-monitor
#
# monitors the page and prints out when things change
import time, re, datetime
from commonssite.scrapers import veris2

INTERVAL = 5.0 # seconds

thresholds = {
	'kW' : 1.0,
	'kWh' : 1.0,
	'Volts' : 1.0,
	'Amps' : 1.0,
	'' : .1,
	'Hz': 0.5,
	'Default' : 0.0
}

ignore = ['Hz', '', 'Default']

unit_parser = re.compile(r'[^(]+\((\w*)\)')

def unit(name):
	try:
		return unit_parser.match(name).group(1)
	except:
		return 'Default'

def thresh(name):
	return thresholds.get(unit(name), 0.0)

def changed(name, val1, val2):
	if name == 'Time' or unit(name) in ignore:
		return False
	th = thresh(name)
	try:
		return abs(float(val2) - float(val1)) > th
	except:
		return val1 != val2

class Monitor:

	last2 = {}
	last3 = {}
	last4 = {}
	nupdates = 0

	def get_new_data(self):
		update_dict = {
			'Device 2' : [],
			'Device 3' : [],
			'Device 4' : []
		}
		print "getting update #%d" % self.nupdates, datetime.datetime.now()
		# get latest
		d2, d3, d4 = veris2.get_data()
		# compare to last_data
		if self.nupdates != 0:
			for header, value in d2.iteritems():
				if changed(header, self.last2.get(header), value):
					print "Device 2,", header.ljust(30, ' '), self.last2.get(header,'').ljust(6,' '), " ==> ", d2.get(header)
					update_dict['Device 2'].append((header, last2.get(header), d2.get(header)))
			for header, value in d3.iteritems():
				if changed(header, self.last3.get(header), value):
					print "Device 3,", header.ljust(30, ' '), self.last3.get(header,'').ljust(6,' '), " ==> ", d3.get(header)
					update_dict['Device 3'].append((header, last3.get(header), d3.get(header)))
			for header, value in d4.iteritems():
				if changed(header, self.last4.get(header), value):
					print "Device 4,", header.ljust(30, ' '), self.last4.get(header,'').ljust(6,' '), " ==> ", d4.get(header)
					update_dict['Device 4'].append((header, last4.get(header), d4.get(header)))
		self.last2 = d2
		self.last3 = d3
		self.last4 = d4
		self.nupdates += 1
		return update_dict

	def serialize(self):
		return (self.nupdates, self.last2, self.last3, self.last4)

	@classmethod
	def deserialize(cls, ser):
		m = Monitor()
		m.nupdates, m.last2, m.last3, m.last4 = ser
		return m

if __name__ == '__main__':
	from sys import argv
	sleepstyle = True
	if len(argv) > 1:
		opt = argv[1]
		sleepstyle = (opt != '-e')
	m = Monitor()
	while True:
		try:
			m.get_new_data()
			if sleepstyle:
				print "next update in %f seconds" % INTERVAL
				time.sleep(INTERVAL)
			else:
				print "press Enter for a new reading"
				raw_input()
		except KeyboardInterrupt:
			break
	print "--done--"
