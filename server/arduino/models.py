from timeseries.models import TimeseriesBase
from django.db import models


class GreenhouseDHT(TimeseriesBase):

	hum_east_chimney_low = models.FloatField(null=True, verbose_name="East/Low Solar Chimney Humidity")
	temp_east_chimney_low = models.FloatField(null=True, verbose_name="East/Low Solar Chimney Temperature")
	hum_east_chimney_high = models.FloatField(null=True, verbose_name="East/High Solar Chimney Humidity")
	temp_east_chimney_high = models.FloatField(null=True, verbose_name="East/High Solar Chimney Temperature")
	hum_west_chimney_low = models.FloatField(null=True, verbose_name="West/Low Solar Chimney Humidity")
	temp_west_chimney_low = models.FloatField(null=True, verbose_name="West/Low Solar Chimney Temperature")
	hum_west_chimney_high = models.FloatField(null=True, verbose_name="West/High Solar Chimney Humidity")
	temp_west_chimney_high = models.FloatField(null=True, verbose_name="West/High Solar Chimney Temperature")
	hum_greenhouse_low = models.FloatField(null=True, verbose_name="Greenhouse/Low Humidity")
	temp_greenhouse_low = models.FloatField(null=True, verbose_name="Greenhouse/Low Temperature")
	hum_mezzanine = models.FloatField(null=True, verbose_name="Mezzanine Humidity")
	temp_mezzanine = models.FloatField(null=True, verbose_name="Mezzanine Temperature")
	hum_greenhouse_high = models.FloatField(null=True, verbose_name="Greenhouse/High Humidity")
	temp_greenhouse_high = models.FloatField(null=True, verbose_name="Greenhouse/High Temperature")