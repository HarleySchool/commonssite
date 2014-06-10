# ORM model for Electric/Veris data
from timeseries.models import TimeseriesBase
from django.db import models
import re
from commonssite.settings import veris_sql_table_circuits,	\
	veris_sql_table_device,									\
	datetime_out_format

class Panel(models.Model):
	veris_id = models.IntegerField()
	name = models.CharField(max_length=16)

	def __unicode__(self):
		return unicode(self.name)

class Circuit(models.Model):
	panel = models.ForeignKey('Panel')
	veris_id = models.IntegerField()
	name = models.CharField(max_length=32)

	__re_default_name = re.compile(r'Channel \#\d+')

	def __eq__(self, other):
		return self.id == other.id and self.veris_id == other.veris_id

	def __unicode__(self):
		if Circuit.__re_default_name.match(self.name):
			return u'%s %s' % (unicode(self.panel), self.name)
		else:
			return u'%s' % self.name

class CircuitEntry(TimeseriesBase):
	
	Circuit = models.ForeignKey('Circuit', db_column='circuit_id', default=1)
	Current = models.FloatField(db_column='current')
	Energy = models.FloatField(db_column='energy')
	MaxCurrent = models.FloatField(db_column='current-max')
	Demand = models.FloatField(db_column='demand')
	Power = models.FloatField(db_column='power')
	MaxPower = models.FloatField(db_column='power-max')
	PowerDemand = models.FloatField(db_column='power-demand')
	PowerFactor = models.FloatField(db_column='power-factor')

	def __unicode__(self):
		return u'%s at %s' % (str(self.Circuit), self.Time.strftime(datetime_out_format))

	class Meta:
		db_table = veris_sql_table_circuits
		unique_together = (('Time', 'Circuit'),)

class DeviceSummary(TimeseriesBase):

	Panel = models.ForeignKey('Panel', db_column='panel_id', default=1)
	Frequency = models.FloatField(db_column='frequency')
	LineNeutral = models.FloatField(db_column='line_neutral_3ph')
	LineLine = models.FloatField(db_column='line_line_3ph')
	AToNeutral = models.FloatField(db_column='a_to_neutral')
	BToNeutral = models.FloatField(db_column='b_to_neutral')
	CToNeutral = models.FloatField(db_column='c_to_neutral')
	AToB = models.FloatField(db_column='a_to_b')
	BToC = models.FloatField(db_column='b_to_c')
	CToA = models.FloatField(db_column='c_to_a')
	TotalEnergy = models.FloatField(db_column='total_energy')
	TotalPower = models.FloatField(db_column='total_power')
	TotalPowerFactor = models.FloatField(db_column='total_power_factor')
	AverageCurrent3Phase = models.FloatField(db_column='avg_current')
	Phase1Power = models.FloatField(db_column='phase_1_power')
	Phase2Power = models.FloatField(db_column='phase_2_power')
	Phase3Power = models.FloatField(db_column='phase_3_power')
	Phase1PowerFactor = models.FloatField(db_column='phase_1_power_factor')
	Phase2PowerFactor = models.FloatField(db_column='phase_2_power_factor')
	Phase3PowerFactor = models.FloatField(db_column='phase_3_power_factor')
	Phase1Current = models.FloatField(db_column='phase_1_current')
	Phase2Current = models.FloatField(db_column='phase_2_current')
	Phase3Current = models.FloatField(db_column='phase_3_current')
	PhaseNeutralCurrent = models.FloatField(db_column='phase_neutral_current')
	Phase1Demand = models.FloatField(db_column='phase_1_demand')
	Phase2Demand = models.FloatField(db_column='phase_2_demand')
	Phase3Demand = models.FloatField(db_column='phase_3_demand')
	PhaseNeutralDemand = models.FloatField(db_column='phase_neutral_demand')
	Phase1MaxDemand = models.FloatField(db_column='phase_1_max_demand')
	Phase2MaxDemand = models.FloatField(db_column='phase_2_max_demand')
	Phase3MaxDemand = models.FloatField(db_column='phase_3_max_demand')
	PhaseNeutralMaxDemand = models.FloatField(db_column='phase_neutral_max_demand')
	Demand = models.FloatField(db_column='3ph_demand')
	MaxDemand = models.FloatField(db_column='max_3ph_demand')
	Phase1MaxCurrent = models.FloatField(db_column='phase_1_max_current')
	Phase2MaxCurrent = models.FloatField(db_column='phase_2_max_current')
	Phase3MaxCurrent = models.FloatField(db_column='phase_3_max_current')
	PhaseNeutralMaxCurrent = models.FloatField(db_column='phase_neutral_max_current')
	MaxPower = models.FloatField(db_column='max_3ph_power')

	def __unicode__(self):
		return u'%s summary at %s' % (str(self.Panel), self.Time.strftime(datetime_out_format))

	class Meta:
		db_table = veris_sql_table_device
		unique_together = ('Time', 'Panel')

# CUSTOM CALCULATED FIELDS
class CalculatedStats(TimeseriesBase):
	# Gross = total used
	GrossPowerUsed = models.FloatField(null=True, verbose_name='Gross Power (Consumed)')
	GrossPowerFactorUsed = models.FloatField(null=True, verbose_name='Gross Power Factor (Consumed)')
	GrossEnergyUsed = models.FloatField(null=True, verbose_name='Gross Energy (Consumed)')
	# Gross - total produced
	GrossPowerProduced = models.FloatField(null=True, verbose_name='Gross Power (Produced)')
	GrossPowerFactorProduced = models.FloatField(null=True, verbose_name='Gross Power Factor (Produced)')
	GrossEnergyProduced = models.FloatField(null=True, verbose_name='Gross Energy (Produced)')
	# Net = Gross - (energy produced)
	NetPower = models.FloatField(null=True, verbose_name='Net Power')
	NetEnergy = models.FloatField(null=True, verbose_name='Net Energy')
