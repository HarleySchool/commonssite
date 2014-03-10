# ORM model for Electric/Veris data

from django.db import models
from commonssite.settings import veris_sql_table_channel,	\
	veris_sql_table_device,									\
	datetime_out_format

class ChannelEntry(models.Model):
	
	Time = models.DateTimeField(db_column='time')
	Panel = models.CharField(db_culum='panel')
	Channel = models.CharField(db_column='channel')
	Energy = models.FloatField(db_column='energy')
	Max = models.FloatField(db_column='max')
	Demand = models.FloatField(db_column='demand')
	Power = models.FloatField(db_column='power')
	PowerMax = models.FloatField(db_column='power-max')
	PowerDemand = models.FloatField(db_column='power-demand')
	PowerFactor = models.FloatField(db_column='power-factor')

	def __unicode__(self):
		return u'%s::%s at %s' % (self.Panel, self.Channel, self.Time.strftime(datetime_out_format))

	class Meta:
		db_table = veris_sql_table_channel
		unique_together = ('time', 'channel', 'panel')

class DeviceSummary(models.Model):

	Time = models.DateTimeField(db_column='time')
	Panel = models.CharField(db_culum='panel')
	Frequency = FloatField(db_column='frequency')
	LineNeutral = FloatField(db_column='line_neutral_3ph')
	LineLine = FloatField(db_column='line_neutral_3ph')
	AToNeutral = FloatField(db_column='a_to_neutral')
	BToNeutral = FloatField(db_column='b_to_neutral')
	CToNeutral = FloatField(db_column='c_to_neutral')
	AToB = FloatField(db_column='a_to_b')
	BToC = FloatField(db_column='b_to_c')
	CToA = FloatField(db_column='c_to_a')
	TotalEnergy = FloatField(db_column='total_energy')
	TotalPower = FloatField(db_column='total_power')
	TotalPowerFactor = FloatField(db_column='total_power_factor')
	AverageCurrent3Phase = FloatField(db_column='avg_current')
	Phase1Power = FloatField(db_column='phase_1_power')
	Phase2Power = FloatField(db_column='phase_2_power')
	Phase3Power = FloatField(db_column='phase_3_power')
	Phase1PowerFactor = FloatField(db_column='phase_1_power_factor')
	Phase2PowerFactor = FloatField(db_column='phase_2_power_factor')
	Phase3PowerFactor = FloatField(db_column='phase_3_power_factor')
	Phase1Current = FloatField(db_column='phase_1_current')
	Phase2Current = FloatField(db_column='phase_2_current')
	Phase3Current = FloatField(db_column='phase_3_current')
	PhaseNeutralCurrent = FloatField(db_column='phase_neutral_current')
	Phase1Demand = FloatField(db_column='phase_1_demand')
	Phase2Demand = FloatField(db_column='phase_2_demand')
	Phase3Demand = FloatField(db_column='phase_3_demand')
	PhaseNeutralDemand = FloatField(db_column='phase_neutral_demand')
	Phase1MaxDemand = FloatField(db_column='phase_1_max_demand')
	Phase2MaxDemand = FloatField(db_column='phase_2_max_demand')
	Phase3MaxDemand = FloatField(db_column='phase_3_max_demand')
	PhaseNeutralMaxDemand = FloatField(db_column='phase_neutral_max_demand')
	Demand = FloatField(db_column='3ph_demand')
	MaxDemand = FloatField(db_column='max_3ph_demand')
	Phase1MaxCurrent = FloatField(db_column='phase_1_max_current')
	Phase2MaxCurrent = FloatField(db_column='phase_2_max_current')
	Phase3MaxCurrent = FloatField(db_column='phase_3_max_current')
	PhaseNeutralMaxCurrent = FloatField(db_column='phase_neutral_max_current')
	MaxPower = FloatField(db_column='max_3ph_power')

	def __unicode__(self):
		return u'%s summary at %s' % (self.Panel, self.Time.strftime(datetime_out_format))

	class Meta:
		db_table = veris_sql_table_device
		unique_together = ('time', 'panel')