import datetime, pytz
from timeseries.scrapers import ScraperBase
from dummy.models import DummyModel
import time, random
from math import sin

class DummyScraper(ScraperBase):

	def get_data(self):
		now = pytz.UTC.localize(datetime.datetime.utcnow())
		i = 30.0 + 20.0 * sin(time.time() / 300.0) * random.random()
		c = random.gauss(0.0, 1.0)
		f = 80.0 + 20.0 * sin(time.time() / 300.0)* random.random()
		retlist = [DummyModel(Time=now, interestingness=i, correlations=c, fudge_factor=f)]
		self.status_ok()
		return retlist