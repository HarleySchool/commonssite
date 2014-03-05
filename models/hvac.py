# the ORM objects for HVAC
from commonssite.settings import hvac_sql_table_vrf, hvac_sql_table_erv, datetime_out_format
from django.db import models

DIRECTION_CHOICES = (
	('SWING', 'Swing'),
	('VERTICAL', 'Vertical'),
	('MID-VERTICAL', 'Mid-Vertical'),
	('MID-HORIZONTAL', 'Mid-Horizontal'),
	('HORIZONTAL', 'Horizontal'),
	('MID', 'Mid'),
	('AUTO', 'Auto'))

MODE_CHOICES = (
	('FAN', 'Fan'),
	('COOL', 'Cool'),
	('HEAT', 'Heat'),
	('DRY', 'Dry'),
	('AUTO', 'Auto'),
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
	('LOW', 'Low'), 
	('MID-LOW', 'Mid-Low'),
	('MID-HIGH', 'Mid-High'),
	('HIGH', 'High'),
	('AUTO', 'Auto')
)

class ErvEntry(models.Model):

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

	def __unicode__(self):
		return u'%s at %s' % (self.Name, self.Time.strftime(datetime_out_format))

	class Meta:
		db_table=hvac_sql_table_erv
		unique_together=('time', 'name')

class VrfEntry(models.Model):

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

	def __unicode__(self):
		return u'%s at %s' % (self.Name, self.Time.strftime(datetime_out_format))
	
	class Meta:
		db_table=hvac_sql_table_vrf
		unique_together=('time', 'name')
