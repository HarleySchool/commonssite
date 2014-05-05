from timeseries.models import TimeseriesBase
from django.db import models

class SensorDataPoint(TimeseriesBase):
	sensor = models.ForeignKey('timeseries.ModelRegistry')
	name   = models.CharField(max_length=16)
	svalue = models.TextField(null=True)
	fvalue = models.FloatField(null=True)
	ivalue = models.IntegerField(null=True)

	class Meta:
		unique_together=(('Time','name','sensor'),)