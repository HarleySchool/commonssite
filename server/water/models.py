from django.db import models
from commonssite.server.timeseries.models import TimeseriesBase
class water(TimeseriesBase):
    name = models.CharField(max_length=16)
    val = models.FloatField(null=True)
