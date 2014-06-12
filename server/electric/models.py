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
	Current = models.FloatField(db_column='current', verbose_name=u'Current (A)')
	Energy = models.FloatField(db_column='energy', verbose_name=u'Energy (kWh)')
	MaxCurrent = models.FloatField(db_column='current-max', verbose_name=u'Max Current over 15 min (A)')
	Demand = models.FloatField(db_column='demand', verbose_name=u'Current Demand (A)')
	Power = models.FloatField(db_column='power')
	MaxPower = models.FloatField(db_column='power-max', verbose_name=u'Max Power over 15 min (kW)')
	PowerDemand = models.FloatField(db_column='power-demand', verbose_name=u'Power Demand (kW)')
	PowerFactor = models.FloatField(db_column='power-factor', verbose_name=u'Power Factor')

	def __unicode__(self):
		return u'%s at %s' % (str(self.Circuit), self.Time.strftime(datetime_out_format))

	class Meta:
		db_table = veris_sql_table_circuits
		unique_together = (('Time', 'Circuit'),)

class DeviceSummary(TimeseriesBase):

	Panel = models.ForeignKey('Panel', db_column='panel_id', default=1)
	Frequency = models.FloatField(db_column='frequency', verbose_name=u'Frequency (Hz)')
	LineNeutral = models.FloatField(db_column='line_neutral_3ph', verbose_name=u'3-phase line-to-neutral voltage (V)')
	LineLine = models.FloatField(db_column='line_line_3ph', verbose_name=u'3-phase line-to-line voltage (V)')
	AToNeutral = models.FloatField(db_column='a_to_neutral', verbose_name=u'Phase A-to-neutral voltage (V)')
	BToNeutral = models.FloatField(db_column='b_to_neutral', verbose_name=u'Phase B-to-neutral voltage (V)')
	CToNeutral = models.FloatField(db_column='c_to_neutral', verbose_name=u'Phase C-to-neutral voltage (V)')
	AToB = models.FloatField(db_column='a_to_b', verbose_name=u'Phase A-to-Phase B Voltage (V)')
	BToC = models.FloatField(db_column='b_to_c', verbose_name=u'Phase B-to-Phase C Voltage (V)')
	CToA = models.FloatField(db_column='c_to_a', verbose_name=u'Phase C-to-Phase A Voltage (V)')
	TotalEnergy = models.FloatField(db_column='total_energy', verbose_name=u'Total Panel Energy (kWh)')
	TotalPower = models.FloatField(db_column='total_power', verbose_name=u'Total Panel Power (kW)')
	TotalPowerFactor = models.FloatField(db_column='total_power_factor', verbose_name=u'Total Panel Power Factor')
	Demand = models.FloatField(db_column='3ph_demand', verbose_name=u'Toal Panel Demand (kW)')
	MaxDemand = models.FloatField(db_column='max_3ph_demand', verbose_name=u'Toal Panel Max-Demand over 15 min (kW)')
	MaxPower = models.FloatField(db_column='max_3ph_power', verbose_name=u'Toal Panel Max-Power over 15 min (kW)')
	AverageCurrent3Phase = models.FloatField(db_column='avg_current', verbose_name=u'Average Panel Current (A)')
	Phase1Power = models.FloatField(db_column='phase_1_power', verbose_name=u'Phase A Power (kW)')
	Phase2Power = models.FloatField(db_column='phase_2_power', verbose_name=u'Phase B Power (kW)')
	Phase3Power = models.FloatField(db_column='phase_3_power', verbose_name=u'Phase C Power (kW)')
	Phase1PowerFactor = models.FloatField(db_column='phase_1_power_factor', verbose_name=u'Phase A Power Factor')
	Phase2PowerFactor = models.FloatField(db_column='phase_2_power_factor', verbose_name=u'Phase B Power Factor')
	Phase3PowerFactor = models.FloatField(db_column='phase_3_power_factor', verbose_name=u'Phase C Power Factor')
	Phase1Current = models.FloatField(db_column='phase_1_current', verbose_name=u'Phase A Current (A)')
	Phase2Current = models.FloatField(db_column='phase_2_current', verbose_name=u'Phase B Current (A)')
	Phase3Current = models.FloatField(db_column='phase_3_current', verbose_name=u'Phase C Current (A)')
	PhaseNeutralCurrent = models.FloatField(db_column='phase_neutral_current', verbose_name=u'Neutral Line Current (A)')
	Phase1Demand = models.FloatField(db_column='phase_1_demand', verbose_name=u'Phase A Demand (kW)')
	Phase2Demand = models.FloatField(db_column='phase_2_demand', verbose_name=u'Phase B Demand (kW)')
	Phase3Demand = models.FloatField(db_column='phase_3_demand', verbose_name=u'Phase C Demand (kW)')
	PhaseNeutralDemand = models.FloatField(db_column='phase_neutral_demand', verbose_name=u'Neutral Line Demand (kW)')
	Phase1MaxDemand = models.FloatField(db_column='phase_1_max_demand', verbose_name=u'Phase A Max Demand over 15 min (kW)')
	Phase2MaxDemand = models.FloatField(db_column='phase_2_max_demand', verbose_name=u'Phase B Max Demand over 15 min (kW)')
	Phase3MaxDemand = models.FloatField(db_column='phase_3_max_demand', verbose_name=u'Phase C Max Demand over 15 min (kW)')
	PhaseNeutralMaxDemand = models.FloatField(db_column='phase_neutral_max_demand', verbose_name=u'Neutral Line Max Demand over 15 min (kW)')
	Phase1MaxCurrent = models.FloatField(db_column='phase_1_max_current', verbose_name=u'Phase A Max Current over 15 min (A)')
	Phase2MaxCurrent = models.FloatField(db_column='phase_2_max_current', verbose_name=u'Phase B Max Current over 15 min (A)')
	Phase3MaxCurrent = models.FloatField(db_column='phase_3_max_current', verbose_name=u'Phase C Max Current over 15 min (A)')
	PhaseNeutralMaxCurrent = models.FloatField(db_column='phase_neutral_max_current', verbose_name=u'Neutral Line Max Current over 15 min (A)')

	def __unicode__(self):
		return u'%s summary at %s' % (str(self.Panel), self.Time.strftime(datetime_out_format))

	class Meta:
		db_table = veris_sql_table_device
		unique_together = ('Time', 'Panel')

# CUSTOM CALCULATED FIELDS
class CalculatedStats(TimeseriesBase):
	# Gross = total used
	GrossPowerUsed = models.FloatField(null=True, verbose_name='Gross Power Consumed (kW)')
	GrossEnergyUsed = models.FloatField(null=True, verbose_name='Gross Energy Consumed (kWh)')
	# Gross - total produced
	GrossPowerProduced = models.FloatField(null=True, verbose_name='Gross Power Produced (kW)')
	GrossEnergyProduced = models.FloatField(null=True, verbose_name='Gross Energy Produced (kWh)')
	# Net = Gross - (energy produced)
	NetPower = models.FloatField(null=True, verbose_name='Net Power (kW)')
	NetEnergy = models.FloatField(null=True, verbose_name='Net Energy (kWh)')
