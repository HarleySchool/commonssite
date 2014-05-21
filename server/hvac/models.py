# the ORM objects for HVAC
from timeseries.models import TimeseriesBase
from commonssite.settings import hvac_sql_table_vrf, hvac_sql_table_erv, datetime_out_format
from django.db import models

class Rooms(models.Model):
	name = models.CharField(max_length=32)

	def __unicode__(self):
		return u'%s' % self.name

class FanSpeeds(models.Model):
	value = models.CharField(max_length=8)

	def __unicode__(self):
		return u'%s' % self.value

class Modes(models.Model):
	value = models.CharField(max_length=12)

	def __unicode__(self):
		return u'%s' % self.value

class FanDirections(models.Model):
	value = models.CharField(max_length=14)

	def __unicode__(self):
		return u'%s' % self.value

class ErvEntry(TimeseriesBase):
	Name = models.ForeignKey('Rooms', db_column='name', default=1)
	AirDirection = models.ForeignKey('FanDirections', db_column='air direction', default=1)
	FanSpeed = models.ForeignKey('FanSpeeds', db_column='fan speed', default=1)
	Mode = models.ForeignKey('Modes', db_column='mode', default=1)
	ErrorSign = models.BooleanField(db_column='error')
	InletTemp = models.FloatField(db_column='measured temp', verbose_name=u'Measured Temperature')
	Running = models.NullBooleanField(db_column='running')

	def __unicode__(self):
		return u'%s at %s' % (self.Name, self.Time.strftime(datetime_out_format))

	class Meta:
		db_table=hvac_sql_table_erv
		unique_together=('Time', 'Name')

class VrfEntry(TimeseriesBase):
	Name = models.ForeignKey('Rooms', db_column='name', default=1)
	AirDirection = models.ForeignKey('FanDirections', db_column='air direction', default=1)
	FanSpeed = models.ForeignKey('FanSpeeds', db_column='fan speed', default=1)
	Mode = models.ForeignKey('Modes', db_column='mode', default=1)
	ErrorSign = models.BooleanField(db_column='error')
	InletTemp = models.FloatField(db_column='measured temp')
	HeatMax = models.FloatField(db_column='heat max')
	HeatMin = models.FloatField(db_column='heat min')
	CoolMax = models.FloatField(db_column='cool max')
	CoolMin = models.FloatField(db_column='cool min')
	AutoMax = models.FloatField(db_column='auto max')
	AutoMin = models.FloatField(db_column='auto min')
	SetTemp = models.FloatField(db_column='set temp', verbose_name=u'Set Temperature')
	Running = models.NullBooleanField(db_column='running')

	def __unicode__(self):
		return u'%s at %s' % (self.Name, self.Time.strftime(datetime_out_format))
	
	class Meta:
		db_table=hvac_sql_table_vrf
		unique_together=('Time', 'Name')
