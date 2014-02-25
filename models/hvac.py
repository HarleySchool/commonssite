# the ORM objects for HVAC
from commonssite.settings import hvac_sql_table_vrf, hvac_sql_table_erv
from commonssite.models.db import db
from peewee import *

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
		db_table=hvac_sql_table_vrf

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
		db_table=hvac_sql_table_erv
