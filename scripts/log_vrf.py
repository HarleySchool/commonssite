#!/home/dataupload/.virtualenv/Django/bin/python
from commonssite.server.timeseries.models import ModelRegistry
from commonssite.server.hvac.models import VrfEntry
from commonssite.server.hvac.scrapers import ScraperVRF

# get corresponding modelregistry entry
reg = ModelRegistry.objects.get(id=2)

# create scraper instance
scraper = ScraperVRF(VrfEntry, reg)

# get data
scraper.get_and_save_single()