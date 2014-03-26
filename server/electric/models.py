# ORM model for Electric/Veris data

from django.db import models
from commonssite.settings import veris_sql_table_channel,	\
	veris_sql_table_device,									\
	veris_sql_table_map,									\
	datetime_spreadsheet_format

class ChannelNameMap(models.Model):

	Panel = models.CharField(db_column='panel', max_length=16)
	Channel = models.CharField(db_column='channel', max_length=32)
	Name = models.CharField(db_column='name', max_length=32)

	def __unicode__(self):
		return u'%s => %s' % (self.Channel, self.Name)

	class Meta:
		db_table = veris_sql_table_map
		unique_together = ('Panel', 'Channel')

class ChannelEntry(models.Model):
	
	Time = models.DateTimeField(db_column='time')
	Panel = models.CharField(db_column='panel', max_length=16)
	Channel = models.CharField(db_column='channel', max_length=32)
	Current = models.FloatField(db_column='current')
	Energy = models.FloatField(db_column='energy')
	MaxCurrent = models.FloatField(db_column='current-max')
	Demand = models.FloatField(db_column='demand')
	Power = models.FloatField(db_column='power')
	MaxPower = models.FloatField(db_column='power-max')
	PowerDemand = models.FloatField(db_column='power-demand')
	PowerFactor = models.FloatField(db_column='power-factor')

	def __unicode__(self):
		return u'%s::%s at %s' % (self.Panel, self.Channel, self.Time.strftime(datetime_spreadsheet_format))

	@classmethod
	def fields(cls):
		"""return list of names of non-unique fields (i.e. everything except 'time' and 'name'). Useful in automatically creating objects"""
		return ['Channel', 'Panel', 'Current', 'Energy', 'MaxCurrent', 'Demand', 'Power', 'MaxPower', 'PowerDemand', 'PowerFactor']

	@classmethod
	def all_headers(cls):
		headers = ['Time']
		headers.extend(cls.fields())
		return headers

	class Meta:
		db_table = veris_sql_table_channel
		unique_together = (('Time', 'Channel', 'Panel'),)

class DeviceSummary(models.Model):

	Time = models.DateTimeField(db_column='time')
	Panel = models.CharField(db_column='panel', max_length=16)
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
		return u'%s summary at %s' % (self.Panel, self.Time.strftime(datetime_spreadsheet_format))

	@classmethod
	def fields(cls):
		"""return list of names of non-unique fields (i.e. everything except 'time' and 'name'). Useful in automatically creating objects"""
		return ['Panel', 'Frequency', 'LineNeutral', 'LineLine', 'AToNeutral', 'BToNeutral', 'CToNeutral', 'AToB', 'BToC', 'CToA', 'TotalEnergy', 'TotalPower', 'TotalPowerFactor', 'AverageCurrent3Phase', 'Phase1Power', 'Phase2Power', 'Phase3Power', 'Phase1PowerFactor', 'Phase2PowerFactor', 'Phase3PowerFactor', 'Phase1Current', 'Phase2Current', 'Phase3Current', 'PhaseNeutralCurrent', 'Phase1Demand', 'Phase2Demand', 'Phase3Demand', 'PhaseNeutralDemand', 'Phase1MaxDemand', 'Phase2MaxDemand', 'Phase3MaxDemand', 'PhaseNeutralMaxDemand', 'Demand', 'MaxDemand', 'Phase1MaxCurrent', 'Phase2MaxCurrent', 'Phase3MaxCurrent', 'PhaseNeutralMaxCurrent', 'MaxPower']

	@classmethod
	def all_headers(cls):
		headers = ['Time']
		headers.extend(cls.fields())
		return headers

	class Meta:
		db_table = veris_sql_table_device
		unique_together = ('Time', 'Panel')
