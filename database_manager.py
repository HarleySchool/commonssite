from peewee import *

# load database configuration
with open('/home/dataupload/sql_creds.txt', 'r') as creds:
	db_host = creds.readline()
	uname = creds.readline()
	pw = creds.readline()
db = MySQLDatabase("commons.db", host=db_host, user=uname, passwd=pw)

#################
## HVAC SCHEMA ##
#################

direction_field = [
	('Swing', 'Swing'),
	('Vertical', 'Vertical'),
	('Mid-Vertical', 'Mid-Vertical'),
	('Mid-Horizontal', 'Mid-Horizontal'),
	('Horizontal', 'Horizontal'),
	('Mid', 'Mid'),
	('Auto', 'Auto')
]

mode_field = [
	('Fan', 'Fan'),
	('Cool', 'Cool'),
	('Heat', 'Heat'),
	('Dry', 'Dry'),
	('Auto', 'Auto'),
	('BAHP', 'BAHP'),
	('AUTOCOOL', 'AUTOCOOL'),
	('AUTOHEAT', 'AUTOHEAT'),
	('VENTILATE', 'VENTILATE'),
	('PANECOOL', 'PANECOOL'),
	('PANEHEAT', 'PANEHEAT'),
	('OUTCOOL', 'OUTCOOL'),
	('DEFLOST', 'DEFLOST'),
	('HEATRECOVERY', 'HEATRECOVERY'),
	('BYPASS', 'BYPASS'),
	('LC_AUTO', 'LC_AUTO')
]

speed_field = [
	('Low', 'Low'), 
	('Mid-Low', 'Mid-Low'),
	('Mid-High', 'Mid-High'),
	('High', 'High'),
	('Auto', 'Auto')
]

class VrfEntry(Model):
	Time = DateTimeField(db_column='time')
	Name = CharField(db_column='name')
	AirDirection = CharField(db_column='air direction', choices=direction_field)
	FanSpeed = CharField(db_column='fan speed', choices=speed_field)
	Mode = CharField(db_column='mode', choices=mode_field)
	ErrorSign = BooleanField(db_column='error')
	HeatMax = FloatField(db_column='heat max')
	HeatMin = FloatField(db_column='heat min')
	CoolMax = FloatField(db_column='cool max')
	CoolMin = FloatField(db_column='cool min')
	AutoMax = FloatField(db_column='auto max')
	AutoMin = FloatField(db_column='auto min')
	SetTemp = FloatField(db_column='set temp')
	InletTemp = FloatField(db_column='measured temp')

	class Meta:
		database = db
		primary_key = CompositeKey('Time', 'Name')

class ErvEntry(Model):
	Time = DateTimeField(db_column='time')
	Name = CharField(db_column='name')
	AirDirection = CharField(db_column='air direction', choices=direction_field)
	FanSpeed = CharField(db_column='fan speed', choices=speed_field)
	Mode = CharField(db_column='mode', choices=mode_field)
	ErrorSign = BooleanField(db_column='error')
	InletTemp = FloatField(db_column='measured temp')

	class Meta:
		database = db
		primary_key = CompositeKey('Time', 'Name')

if __name__ == '__main__':
	import datetime

	now = datetime.datetime.now()
	# add test rows to each table
	vrf_inst = VrfEntry(
		Time=now,
		Name='Test-VRF',
		AirDirection=direction_field[1],
		FanSpeed=speed_field[1],
		Mode=mode_field[1],
		ErrorSign=False,
		HeatMin=67.0,
		HeatMax=76.0,
		CoolMin=60.0,
		CoolMax=68.0,
		AutoMin=62.0,
		AutoMax=72.0,
		SetTemp=68.0,
		InletTemp=72.0
	)
	erv_inst = VrfEntry(
		Time=now,
		Name='Test-ERV',
		AirDirection=direction_field[1],
		FanSpeed=speed_field[1],
		Mode=mode_field[1],
		ErrorSign=False,
		InletTemp=72.0
	)
	print "created instances. saving."
	vrf_inst.save()
	erv_inst.save()
