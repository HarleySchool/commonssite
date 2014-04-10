# hvac migrator
#
# data was logged locally in CSV format for a while. This script uploads these files to the sql database

# peewee is the database-handling module.
from peewee import *
import csv, re, datetime
from commonssite.server.hvac.models import *
from commonssite.server.hvac.scrapers import group_id_to_name

SEP = '\t'
date_re = re.compile(r'(\d+)-(\d+)-(\d+)\ (\d+):(\d+)')

def dateparse(datestring):
	parsed = date_re.match(datestring)
	return datetime.datetime(int(parsed.group(3)), int(parsed.group(1)), int(parsed.group(2)), int(parsed.group(4)), int(parsed.group(5)))

# example file (first few rows):
"""
Timestamp	Group	SetTemp	InletTemp	CoolMin	CoolMax	HeatMin	HeatMax	AutoMin	AutoMax	Mode	FanSpeed
2-3-2014 8:35	1	72.5	71.6	66.2	73.4	62.6	73.4	66.2	73.4	HEAT	MID-LOW
2-3-2014 8:35	2	72.5	71.6	66.2	73.4	62.6	73.4	66.2	73.4	HEAT	HIGH
2-3-2014 8:35	3	71.6	68.9	66.2	73.4	62.6	73.4	66.2	73.4	AUTOHEAT	MID-LOW
2-3-2014 8:35	4	71.6	70.7	66.2	73.4	62.6	73.4	66.2	73.4	AUTOHEAT	MID-LOW
2-3-2014 8:35	5	72.5	69.8	66.2	73.4	62.6	73.4	66.2	73.4	HEAT	HIGH
2-3-2014 8:35	6	71.6	69.8	66.2	73.4	62.6	73.4	66.2	73.4	HEAT	HIGH
2-3-2014 8:35	7	72.5	71.6	66.2	73.4	62.6	73.4	66.2	73.4	HEAT	HIGH
2-3-2014 8:35	8	71.6	65.3	66.2	73.4	62.6	73.4	66.2	73.4	HEAT	MID-LOW
2-3-2014 8:35	9	71.6	68.9	66.2	73.4	62.6	73.4	66.2	73.4	AUTOHEAT	MID-LOW
 .
 .
etc
"""

class HvacMigrator(object):

	@classmethod
	def migrate(cls, csv_file):
		with open(csv_file, 'r') as f:
			reader = csv.reader(f, delimiter=SEP)
			headers = None

			def get_val(r, name):
				return r[header_map[name]]

			for row in reader:
				if not headers:
					headers=row
					header_map = dict(zip(headers, range(len(headers))))
				else:
					try:
						model = {}
						model['Time'] = dateparse(get_val(row, 'Timestamp'))
						model['Name'] = group_id_to_name(int(get_val(row, 'Group')))
						if model['Name'].find('ERV') == -1:
							cls = VrfEntry
						else:
							cls = ErvEntry
						for h in headers:
							# timestamp and group were already handled as special cases
							if h == 'Timestamp' or h == 'Group':
								continue
							try:
								# try parsing as float
								model[h] = float(get_val(row, h))
							except:
								if get_val(row,h) == 'None':
									model[h] = None
								else:
									# default to string
									model[h] = get_val(row, h)
						obj = cls(**model)
						try:
							obj.save(force_insert=True)
						except IntegrityError:
							print model['Name'], model['Time'], "has already been saved"
						print "saved %s" % model['Name'], model['Time']
					except:
						print "random error?"
		print "--done--"
