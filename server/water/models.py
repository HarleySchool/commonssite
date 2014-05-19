from django.db import models
from commonssite.server.timeseries.models import TimeseriesBase
class water(TimeseriesBase):
	t1 = models.IntegerField(verbose_name='T1 (*C)')
	t2 = models.IntegerField(verbose_name='T2 (*C)')
	t3 = models.IntegerField(verbose_name='T3 (*C)')
	t4 = models.IntegerField(verbose_name='T4 (*C)')
	t5 = models.IntegerField(verbose_name='T5 (*C)')
	flow = models.FloatField(verbose_name='Flow')
	pressure = models.FloatField(verbose_name='Pressure')
	pump1 = models.IntegerField(verbose_name='Pump 1 (%)')
	pump2 = models.IntegerField(verbose_name='Pump 2 (%)')
	pump3 = models.IntegerField(verbose_name='Pump 3 (on/off)')
	accnrj = models.IntegerField(verbose_name='Acc. NRJ')
	acch = models.IntegerField(verbose_name='Acc. H')
	accflow = models.IntegerField(verbose_name='Acc. Flow')


