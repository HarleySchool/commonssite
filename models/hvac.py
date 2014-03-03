# the ORM objects for HVAC
from commonssite.settings import hvac_sql_table_vrf, hvac_sql_table_erv
from commonssite.models.db import db
from django.db import models

class ErvEntry(models.Model):

	DIRECTION_CHOICES = (
		('Swing', 'Swing'),
		('Vertical', 'Vertical'),
		('Mid-Vertical', 'Mid-Vertical'),
		('Mid-Horizontal', 'Mid-Horizontal'),
		('Horizontal', 'Horizontal'),
		('Mid', 'Mid'),
		('Auto', 'Auto'))

	MODE_CHOICES = (
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
	)

	SPEED_CHOICES = (
		('Low', 'Low'), 
		('Mid-Low', 'Mid-Low'),
		('Mid-High', 'Mid-High'),
		('High', 'High'),
		('Auto', 'Auto')
	)

	Time = models.DateTimeField(db_column='time')
	Name = models.CharField(db_column='name', max_length=32)
	AirDirection = models.CharField(db_column='air direction', choices=DIRECTION_CHOICES, max_length=12)
	FanSpeed = models.CharField(db_column='fan speed', choices=SPEED_CHOICES, max_length=8)
	Mode = models.CharField(db_column='mode', choices=MODE_CHOICES, max_length=14)
	ErrorSign = models.BooleanField(db_column='error')
	InletTemp = models.FloatField(db_column='measured temp')
	
	@classmethod
	def fields(cls):
		"""return list of names of non-unique fields (i.e. everything except 'time' and 'name'). Useful in automatically creating objects"""
		return ['AirDirection','FanSpeed','Mode','ErrorSign','InletTemp']

	@classmethod
	def all_headers(cls):
		headers = ['Time', 'Name']
		headers.extend(cls.fields())
		return headers

	class Meta:
		db_table=hvac_sql_table_erv
		unique_together=('time', 'name')

class VrfEntry(models.Model):

	DIRECTION_CHOICES = (
		('Swing', 'Swing'),
		('Vertical', 'Vertical'),
		('Mid-Vertical', 'Mid-Vertical'),
		('Mid-Horizontal', 'Mid-Horizontal'),
		('Horizontal', 'Horizontal'),
		('Mid', 'Mid'),
		('Auto', 'Auto'))

	MODE_CHOICES = (
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
	)

	SPEED_CHOICES = (
		('Low', 'Low'), 
		('Mid-Low', 'Mid-Low'),
		('Mid-High', 'Mid-High'),
		('High', 'High'),
		('Auto', 'Auto')
	)

	Time = models.DateTimeField(db_column='time')
	Name = models.CharField(db_column='name', max_length=32)
	AirDirection = models.CharField(db_column='air direction', choices=DIRECTION_CHOICES, max_length=12)
	FanSpeed = models.CharField(db_column='fan speed', choices=SPEED_CHOICES, max_length=8)
	Mode = models.CharField(db_column='mode', choices=MODE_CHOICES, max_length=14)
	ErrorSign = models.BooleanField(db_column='error')
	InletTemp = models.FloatField(db_column='measured temp')
	HeatMax = models.FloatField(db_column='heat max')
	HeatMin = models.FloatField(db_column='heat min')
	CoolMax = models.FloatField(db_column='cool max')
	CoolMin = models.FloatField(db_column='cool min')
	AutoMax = models.FloatField(db_column='auto max')
	AutoMin = models.FloatField(db_column='auto min')
	SetTemp = models.FloatField(db_column='set temp')

	@classmethod
	def fields(cls):
		"""return list of names of non-unique fields (i.e. everything except 'time' and 'name'). Useful in automatically creating objects"""
		return ['AirDirection','FanSpeed','Mode','ErrorSign','HeatMax','HeatMin','CoolMax','CoolMin','AutoMax','AutoMin','SetTemp','InletTemp']

	@classmethod
	def all_headers(cls):
		headers = ['Time', 'Name']
		headers.extend(cls.fields())
		return headers
	
	class Meta(ErvEntry.Meta):
		db_table=hvac_sql_table_vrf
		unique_together=('time', 'name')