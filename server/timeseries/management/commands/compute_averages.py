# this file defines a django management command that logs a data point
# for each system. This command can (and should) be scheduled to run
# periodically (every minute or so), for example using cron.
#
# Data logged by this comand are all marked as 'temporary'. Separately
# the log_average command must be used to aggregate and permanently
# store data.
#
# usage:
# python manage.py log_now

import threading
from django.core.management.base import BaseCommand, CommandError
from commonssite.server.timeseries.models import ModelRegistry
from commonssite.server.timeseries.helpers import get_registered_scraper, get_registered_model

class Command(BaseCommand):

	help = 'Logs a single \'permanent\' data point for all registered systems calculated as the average of data since the last time this was run'

	def handle(self, *args, **options):
		# get all registered scrapers from the database (a small query)
		scrapers_models = [(get_registered_scraper(r.scraper_class), get_registered_model(r.model_class), r) for r in ModelRegistry.objects.all()]
		threads = [None] * len(scrapers_models)
		for i, (scraper_class, model_class, registry) in enumerate(scrapers_models):
			# Initialize scraper object
			scraperinst = scraper_class(model_class, registry)
			# spawn a thread for each scraper so that any I/O blockage doesn't stall the whole system
			threads[i] = threading.Thread(target=scraperinst.compute_average_of_temporaries)
			threads[i].start()
		for th in threads:
			th.join()
		print "-LOGGING DONE-"
