from django.core.management.base import BaseCommand, CommandError
from commonssite.scrapers import *

class Command(BaseCommand):
    args = 'start [hvac] [veris]'
    help = 'start logging the specified scrapers into the database' 

    def __map_name(self, n):
	mapping = {
		'hvac' : ScraperHvac,
		'veris' : ScraperElectric,
		'electric' : ScraperElectric
	}    

    def handle(self, *args, **options):
	lc_args = map(lambda s: s.lower(), args)
	# TODO a stop command
	if len(lc_args) > 0:
		if lc_args[0] == 'start':
			for scrape in lc_args[1:]:
				sc_obj = self.__map_name(scrape)
				if sc_obj:
					Logger(sc_obj, 20*60).start()
					self.stdout.write("starting %s scraper" % scrape)
				else:
					self.stdout.write("no scraper by the name of %s" : scrape)

