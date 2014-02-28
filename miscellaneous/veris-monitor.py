# veris-monitor
#
# monitors the page and prints out when things change
import time, re
from commonssite.scrapers import veris2

INTERVAL = 5.0 # seconds

thresholds = {
	'kW' : 1.0,
	'kWh' : 1.0,
	'Volts' : 1.0,
	'Amps' : 1.0,
	'' : .1,
	'Hz': 0.1,
	'Default' : 0.0
}

unit_parser = re.compile(r'[^(]+\((\w*)\)')

def unit(name):
	try:
		return unit_parser.match(name).group(1)
	except:
		return 'Default'

def thresh(name):
	return thresholds.get(unit(name), 0.0)

def changed(name, val1, val2):
	if name == 'Time':
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
		print "getting update #%d" % self.nupdates
		# get latest
		d2, d3, d4 = veris2.get_data()
		# compare to last_data
		if self.nupdates == 0:
			for header, value in d2.iteritems():
				self.last2[header] = value
			for header, value in d3.iteritems():
				self.last3[header] = value
			for header, value in d4.iteritems():
				self.last4[header] = value
		else:
			for header, value in d2.iteritems():
				if changed(header, self.last2.get(header), value):
					print "Device 2,", header.ljust(30, ' '), self.last2.get(header,'').ljust(6,' '), " ==> ", d2.get(header)
					self.last2[header] = value
			for header, value in d3.iteritems():
				if changed(header, self.last3.get(header), value):
					print "Device 3,", header.ljust(30, ' '), self.last3.get(header,'').ljust(6,' '), " ==> ", d3.get(header)
					self.last3[header] = value
			for header, value in d4.iteritems():
				if changed(header, self.last4.get(header), value):
					print "Device 4,", header.ljust(30, ' '), self.last4.get(header,'').ljust(6,' '), " ==> ", d4.get(header)
					self.last4[header] = value
		self.nupdates += 1

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
