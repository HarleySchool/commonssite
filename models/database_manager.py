from peewee import *
from commonssite.settings import sql_credentials

# load database configuration
with open(sql_credentials, 'r') as creds:
	db_host = creds.readline().strip()
	uname = creds.readline().strip()
	pw = creds.readline().strip()
db = MySQLDatabase("commons", host=db_host, user=uname, passwd=pw)

if __name__ == '__main__':
	import datetime

	now = datetime.datetime.now()
	# add test rows to each table
	vrf_inst = VrfEntry(
		Time=now,
		Name='Test-VRF',
		AirDirection=direction_field[1][0],
		FanSpeed=speed_field[1][0],
		Mode=mode_field[1][0],
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
	erv_inst = ErvEntry(
		Time=now,
		Name='Test-ERV',
		AirDirection=direction_field[1][0],
		FanSpeed=speed_field[1][0],
		Mode=mode_field[1][0],
		ErrorSign=False,
		InletTemp=72.0
	)
	erv_inst2 = ErvEntry(
		Time=now,
		Name='Test2-ERV',
		AirDirection=direction_field[1][0],
		FanSpeed=speed_field[1][0],
		Mode=mode_field[1][0],
		ErrorSign=False,
		InletTemp=72.0
	)
	print "created instances. saving."
	vrf_inst.save(force_insert=True)
	erv_inst.save(force_insert=True)
	erv_inst2.save(force_insert=True)
