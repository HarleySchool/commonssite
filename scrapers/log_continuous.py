from commonssite.server.timeseries.models import ModelRegistry
from commonssite.server.timeseries.helpers import get_registered_scraper, get_registered_model
from haystack.management.commands import update_index
from log import scheduler

if __name__ == '__main__':
	cron = scheduler()
	# Get lists of scrapers/models
	scrapers_models = [(get_registered_scraper(r.scraper_class), get_registered_model(r.model_class), r) for r in ModelRegistry.objects.all()]
	for scraper_class, model_class, registry in scrapers_models:
		# Initialize all of them
		scraperinst = scraper_class(model_class, registry)
		# Register with the scheduler the quick task of marking values as permanent
		# TODO - make this threadsafe! we can't have new models going in while marking other models as most-recent
		cron.register(scraperinst.compute_average_of_temporaries, 1200, '%s permanent marker' % (scraperinst.__class__.__name__))
		cron.register(scraperinst.get_and_save_single, 30, scraperinst.__class__.__name__)
		# (hack?) periodically update the search index for projects since tags were difficult to deal with
		# (more specifically, the ManyToMany relation isn't processed by Whoosh immediately)
		cron.register(update_index.Command().handle, 900, "Whoosh index updater")
	# Run the Scheduler (forever)
	cron.main()
