from django.db import models
from commonssite.server.timeseries.models import TimeseriesBase

class WeatherData(TimeseriesBase):
	uv = models.FloatField(verbose_name=u'UV Index')
	radiation = models.FloatField(verbose_name=u'Solar Radiation (w/m^2)')
	
	barometer = models.FloatField(verbose_name=u'Air Pressure (Hg)', null=True)
	
	dayet = models.FloatField(verbose_name=u'Daily Evapo-Transpiration (in)')
	monthet = models.FloatField(verbose_name=u'Monthly Evapo-Transpiration (in)')
	yearet = models.FloatField(verbose_name=u'Yearly Evapo-Transpiration (in)')
	
	rain = models.FloatField(verbose_name=u'Rainfall since last (in)', null=True)
	rainrate = models.FloatField(verbose_name=u'Rain Rate (in/hr)')
	stormrain = models.FloatField(verbose_name=u'Storm Rain (in)')
	stormstart = models.FloatField(verbose_name=u'Time Storm Started (epoch seconds)', null=True)
	
	dayrain = models.FloatField(verbose_name=u'Daily Rain (in)')
	monthrain = models.FloatField(verbose_name=u'Monthly Rain (in)')
	yearrain = models.FloatField(verbose_name=u'Yearly Rain (in)')
	
	dewpoint = models.FloatField(verbose_name=u'Dew Point (F)')
	heatindex = models.FloatField(verbose_name=u'Heat Index (F)')
	windchill = models.FloatField(verbose_name=u'Wind Chill (F)')
	
	inhumidity = models.FloatField(verbose_name=u'Humidity Inside (%)')
	intemp = models.FloatField(verbose_name=u'Temperature Inside (F)')
	
	outhumidity = models.FloatField(verbose_name=u'Humidity Outside (%)')
	outtemp = models.FloatField(verbose_name=u'Temperature Outside (F)')
	
	sunrise = models.FloatField(verbose_name=u'Sunrise time (secs since midnight)', null=True)
	sunset = models.FloatField(verbose_name=u'Sunset time (secs since midnight)', null=True)
	
	winddir = models.FloatField(verbose_name=u'Wind Direction (degrees CW of north)', null=True)
	windspeed = models.FloatField(verbose_name=u'Wind Speed (mph)')
