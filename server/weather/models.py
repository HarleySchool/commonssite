from django.db import models
from commonssite.server.timeseries.models import TimeseriesBase

# Create your models here.

class weatherdata(TimeseriesBase):
	uv = models.FloatField(null=True)
	barometer = models.FloatField(null=True)
	dayet = models.FloatField(null=True)
	dayrain = models.FloatField(null=True)
	dewpoint = models.FloatField(null=True)
	heatindex = models.FloatField(null=True)
	inhumidity = models.FloatField(null=True)
	intemp = models.FloatField(null=True)
	monthet = models.FloatField(null=True)
	monthrain = models.FloatField(null=True)
	outhumidity = models.FloatField(null=True)
	outtemp = models.FloatField(null=True)
	radiation = models.FloatField(null=True)
	rain = models.FloatField(null=True)
	rainrate = models.FloatField(null=True)
	stormrain = models.FloatField(null=True)
	stormstart = models.FloatField(null=True)
	sunrise = models.FloatField(null=True)
	sunset = models.FloatField(null=True)
	winddir = models.FloatField(null=True)
	windspeed = models.FloatField(null=True)
	windchill = models.FloatField(null=True)
	yearet = models.FloatField(null=True)
	yearrain = models.FloatField(null=True)
