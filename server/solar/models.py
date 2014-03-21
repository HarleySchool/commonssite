from django.db import models
from commonssite.settings import sma_sql_table_panels, sma_sql_table_weather, sma_sql_table_overview

class SMAWeather(models.Model):
	
	Time = models.DateTimeField(db_column='time')
	InternalSolarIrradation = models.FloatField()
	ExternalSolarIrradation = models.FloatField()
	AmbientTemprature = models.FloatField()
	ModuleTemprature = models.FloatField()
	WindVelocity = models.FloatField()

	@classmethod
	def fields(cls):
		"""return list of names of non-unique fields (i.e. everything except 'time' and 'name'). Useful in automatically creating objects"""
		return ['InternalSolarIrradation', 'ExternalSolarIrradation', 'AmbientTemprature', 'ModuleTemprature', 'WindVelocity']

	@classmethod
	def all_headers(cls):
		headers = ['Time']
		headers.extend(cls.fields())
		return headers

	class Meta:
		db_table = sma_sql_table_weather

class SMAOverview(models.Model):

	Time = models.DateTimeField(db_column='time')
	TotalACPower = models.FloatField()
	TotalEnergyToday = models.FloatField()
	TotalEnergy = models.FloatField()
	Message = models.CharField(max_length=128)

	@classmethod
	def fields(cls):
		"""return list of names of non-unique fields (i.e. everything except 'time' and 'name'). Useful in automatically creating objects"""
		return ['TotalACPower', 'TotalEnergyToday', 'TotalEnergy', 'Message']

	@classmethod
	def all_headers(cls):
		headers = ['Time']
		headers.extend(cls.fields())
		return headers

	class Meta:
		db_table = sma_sql_table_overview

class SMAPanels(models.Model):

	Time = models.DateTimeField(db_column='time')
	A_DC_Current = models.FloatField()
	A_DC_Voltage = models.FloatField()
	A_DC_Power = models.FloatField()
	A1_DC_Current = models.FloatField()
	B_DC_Current = models.FloatField()
	B_DC_Voltage = models.FloatField()
	B_DC_Power = models.FloatField()
	B1_DC_Current = models.FloatField()
	TotalYield = models.FloatField()
	GridPhase1Current = models.FloatField()
	GridPhase2Current = models.FloatField()
	GridPhase3Current = models.FloatField()
	GridFrequency = models.FloatField()
	GridPhase1Voltage = models.FloatField()
	GridPhase2Voltage = models.FloatField()
	GridPhase3Voltage = models.FloatField()
	GridDisplacementPowerFactor = models.FloatField()
	GridApparentPower = models.FloatField()
	GridReactivePower = models.FloatField()
	GridPhase1ApparentPower = models.FloatField()
	GridPhase2ApparentPower = models.FloatField()
	GridPhase3ApparentPower = models.FloatField()
	GridPhase1ReactivePower = models.FloatField()
	GridPhase2ReactivePower = models.FloatField()
	GridPhase3ReactivePower = models.FloatField()
	GridPhase1Power = models.FloatField()
	GridPhase2Power = models.FloatField()
	GridPhase3Power = models.FloatField()
	Derating = models.CharField(max_length=10)
	DeviceControlStatus = models.CharField(max_length=8)
	ResidualCurrent = models.FloatField()
	FeedInTime = models.FloatField() # hours
	OperatingTime = models.FloatField() # Hours
	OperationHealth = models.CharField(max_length=16)
	TotalACPower = models.FloatField() # Watts

	@classmethod
	def fields(cls):
		"""return list of names of non-unique fields (i.e. everything except 'time' and 'name'). Useful in automatically creating objects"""
		return ['A_DC_Current', 'A_DC_Voltage', 'A_DC_Power', 'A1_DC_Current', 'B_DC_Current', 'B_DC_Voltage', 'B_DC_Power', 'B1_DC_Current', 'TotalYield', 'GridPhase1Current', 'GridPhase2Current', 'GridPhase3Current', 'GridFrequency', 'GridPhase1Voltage', 'GridPhase2Voltage', 'GridPhase3Voltage', 'GridDisplacementPowerFactor', 'GridApparentPower', 'GridReactivePower', 'GridPhase1ApparentPower', 'GridPhase2ApparentPower', 'GridPhase3ApparentPower', 'GridPhase1ReactivePower', 'GridPhase2ReactivePower', 'GridPhase3ReactivePower', 'GridPhase1Power', 'GridPhase2Power', 'GridPhase3Power', 'Derating', 'DeviceControlStatus', 'ResidualCurrent', 'FeedInTime', 'OperatingTime', 'OperationHealth', 'TotalACPower']

	@classmethod
	def all_headers(cls):
		headers = ['Time']
		headers.extend(cls.fields())
		return headers

	class Meta:
		db_table = sma_sql_table_panels