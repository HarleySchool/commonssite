# ORM objects for the Settings which control scraper behavior

from django.db import models
from commonssite.settings import scrapers_settings_sql_table
import datetime

class ScraperSettings(models.Model):

	Name = models.CharField(db_column='name')
	# Interval is stored as # of minutes
	Interval = models.IntegerField(db_column='interval')

	def timedelta(self):
		return datetime.timedelta(minutes=self.Interval)

	class Meta:
		db_table = scrapers_settings_sql_table