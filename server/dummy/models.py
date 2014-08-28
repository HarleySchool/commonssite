from timeseries.models import TimeseriesBase
from django.db import models

class DummyModel(TimeseriesBase):

	interestingness = models.FloatField(verbose_name="Interestingness")
	correlations = models.FloatField(verbose_name="Correlations")
	fudge_factor = models.FloatField(verbose_name="Fudge Factor (%)")