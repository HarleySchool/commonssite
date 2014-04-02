from django.db import models
from commonssite.server.timeseries.models import TimeseriesBase
from commonssite.settings import sma_sql_table_panels, sma_sql_table_weather, sma_sql_table_overview

class SMAWeather(TimeseriesBase):
	
	InternalSolarIrradation = models.FloatField()
	ExternalSolarIrradation = models.FloatField()
	AmbientTemprature = models.FloatField()
	ModuleTemprature = models.FloatField()
	WindVelocity = models.FloatField()

	class Meta:
		db_table = sma_sql_table_weather

class SMAOverview(TimeseriesBase):

	TotalACPower = models.FloatField()
	TotalEnergyToday = models.FloatField()
	TotalEnergy = models.FloatField()
	Message = models.CharField(max_length=128)

	class Meta:
		db_table = sma_sql_table_overview

class SMAPanels(TimeseriesBase):

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

	class Meta:
		db_table = sma_sql_table_panels