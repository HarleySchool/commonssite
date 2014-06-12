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
	Room = models.ForeignKey('Rooms', db_column='name', default=1)
	AirDirection = models.ForeignKey('FanDirections', db_column='air direction', default=1, verbose_name=u'Air Direction')
	FanSpeed = models.ForeignKey('FanSpeeds', db_column='fan speed', default=1, verbose_name=u'Fan Speed')
	Mode = models.ForeignKey('Modes', db_column='mode', default=1, verbose_name=u'Mode')
	ErrorSign = models.BooleanField(db_column='error', verbose_name=u'Errors')
	InletTemp = models.FloatField(db_column='measured temp', verbose_name=u'Measured Temperature (F)')
	Running = models.NullBooleanField(db_column='running', verbose_name=u'On or Off')

	def __unicode__(self):
		return u'%s at %s' % (self.Room, self.Time.strftime(datetime_out_format))

	class Meta:
		db_table=hvac_sql_table_erv
		unique_together=('Time', 'Room')

class VrfEntry(TimeseriesBase):
	Room = models.ForeignKey('Rooms', db_column='name', default=1)
	AirDirection = models.ForeignKey('FanDirections', db_column='air direction', default=1, verbose_name=u'Air Direction')
	FanSpeed = models.ForeignKey('FanSpeeds', db_column='fan speed', default=1, verbose_name=u'Fan Speed')
	Mode = models.ForeignKey('Modes', db_column='mode', default=1, verbose_name=u'Mode')
	ErrorSign = models.BooleanField(db_column='error', verbose_name=u'Errors')
	InletTemp = models.FloatField(db_column='measured temp', verbose_name=u'Measured Temperature (F)')
	HeatMax = models.FloatField(db_column='heat max', verbose_name=u'Heat-Mode Max Limit (F)')
	HeatMin = models.FloatField(db_column='heat min', verbose_name=u'Heat-Mode Min Limit (F)')
	CoolMax = models.FloatField(db_column='cool max', verbose_name=u'Cool-Mode Max Limit (F)')
	CoolMin = models.FloatField(db_column='cool min', verbose_name=u'Cool-Mode Min Limit (F)')
	AutoMax = models.FloatField(db_column='auto max', verbose_name=u'Auto-Mode Max Limit (F)')
	AutoMin = models.FloatField(db_column='auto min', verbose_name=u'Auto-Mode Min Limit (F)')
	SetTemp = models.FloatField(db_column='set temp', verbose_name=u'Set Temperature (F)')
	Running = models.NullBooleanField(db_column='running', verbose_name=u'On or Off')

	def __unicode__(self):
		return u'%s at %s' % (self.Room, self.Time.strftime(datetime_out_format))
	
	class Meta:
		db_table=hvac_sql_table_vrf
		unique_together=('Time', 'Room')
