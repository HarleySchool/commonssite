from django.db import models
from timeseries.models import TimeseriesBase
from commonssite.settings import sma_sql_table_panels, sma_sql_table_weather, sma_sql_table_overview

class SMAWeather(TimeseriesBase):
	
	# UNUSED InternalSolarIrradation = models.FloatField(verbose_name="") # W/m^2
	ExternalSolarIrradation = models.FloatField(verbose_name="Solar Radiation Levels") # W/m^2
	# UNUSED AmbientTemprature = models.FloatField(verbose_name="") # Celcius
	ModuleTemprature = models.FloatField(verbose_name="Outside Temperature") # celcius
	WindVelocity = models.FloatField(verbose_name="Wind Speed") # m/s

	class Meta:
		db_table = sma_sql_table_weather

class SMAOverview(TimeseriesBase):

	TotalACPower = models.FloatField(verbose_name="Total Power Produced") # W
	TotalEnergyToday = models.FloatField(verbose_name="Daily Yield") # kWh
	TotalEnergy = models.FloatField(verbose_name="Total Yield") # kWh
	# UNUSED, GENERALLY Message = models.CharField(max_length=128)

	class Meta:
		db_table = sma_sql_table_overview

class SMAPanels(TimeseriesBase):

	A_DC_Current = models.FloatField(verbose_name="DC Current, bank A")
	A_DC_Voltage = models.FloatField(verbose_name="DC Voltage, bank A")
	A_DC_Power = models.FloatField(verbose_name="DC Power, bank A")
	A1_DC_Current = models.FloatField(verbose_name="DC Current, bank A1")
	B_DC_Current = models.FloatField(verbose_name="DC Current, bank B")
	B_DC_Voltage = models.FloatField(verbose_name="DC Voltage, bank B")
	B_DC_Power = models.FloatField(verbose_name="DC Power, bank B")
	B1_DC_Current = models.FloatField(verbose_name="DC Current, bank B1")
	# Redundant with Overview TotalYield = models.FloatField(verbose_name="Total Yield")
	GridPhase1Current = models.FloatField(verbose_name="Current to Grid, phase A")
	GridPhase2Current = models.FloatField(verbose_name="Current to Grid, phase B")
	GridPhase3Current = models.FloatField(verbose_name="Current to Grid, phase C")
	GridFrequency = models.FloatField(verbose_name="Grid AC Frequency")
	GridPhase1Voltage = models.FloatField(verbose_name="Grid AC Voltage, phase A")
	GridPhase2Voltage = models.FloatField(verbose_name="Grid AC Voltage, phase B")
	GridPhase3Voltage = models.FloatField(verbose_name="Grid AC Voltage, phase C")
	GridDisplacementPowerFactor = models.FloatField(verbose_name="Grid Displacement Power Factor")
	GridApparentPower = models.FloatField(verbose_name="Grid Apparent Power")
	GridReactivePower = models.FloatField(verbose_name="Grid Reactive Power")
	GridPhase1ApparentPower = models.FloatField(verbose_name="Grid Apparent Power, phase A")
	GridPhase2ApparentPower = models.FloatField(verbose_name="Grid Apparent Power, phase B")
	GridPhase3ApparentPower = models.FloatField(verbose_name="Grid Apparent Power, phase C")
	GridPhase1ReactivePower = models.FloatField(verbose_name="Grid Reactive Power, phase A")
	GridPhase2ReactivePower = models.FloatField(verbose_name="Grid Reactive Power, phase B")
	GridPhase3ReactivePower = models.FloatField(verbose_name="Grid Reactive Power, phase C")
	GridPhase1Power = models.FloatField(verbose_name="Grid Power, phase A")
	GridPhase2Power = models.FloatField(verbose_name="Grid Power, phase B")
	GridPhase3Power = models.FloatField(verbose_name="Grid Power, phase C")
	# UNUSED Derating = models.CharField(max_length=10, verbose_name=u'')
	# UNUSED DeviceControlStatus = models.CharField(max_length=8)
	ResidualCurrent = models.FloatField(verbose_name="Residual Current")
	FeedInTime = models.FloatField(verbose_name="Total Operational Time") # hours
	# REDUNDANT OperatingTime = models.FloatField(verbose_name="") # Hours
	# UNUSED OperationHealth = models.CharField(max_length=16)

	class Meta:
		db_table = sma_sql_table_panels