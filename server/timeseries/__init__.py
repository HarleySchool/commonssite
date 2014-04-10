import dateutil.parser
from dateutil.tz import tzlocal

model_cache = {}
def get_registered_model(class_path):
	"""given the import path for a model (e.g. ModelRegistry.model_class), return the model class"""
	if class_path in model_cache:
		return model_cache[class_path]
	else:
		# import it
		path_parts = class_path.split('.')
		module_path = '.'.join(path_parts[:-1])
		class_name = path_parts[-1]
		mod = __import__(module_path, globals(), locals(), [class_name])
		model_cache[class_path] = getattr(mod, class_name)
		return model_cache[class_path]

scraper_cache = {}
def get_registered_scraper(scraper_path):
	"""given the import path for a scraper (e.g. ModelRegistry.scraper_class), return the scraper class"""
	if scraper_path in scraper_cache:
		return scraper_cache[scraper_path]
	else:
		# import it
		path_parts = scraper_path.split('.')
		module_path = '.'.join(path_parts[:-1])
		class_name = path_parts[-1]
		mod = __import__(module_path, globals(), locals(), [class_name])
		scraper_cache[scraper_path] = getattr(mod, class_name)
		return scraper_cache[scraper_path]

def parse_time(isostring):
	"""Parse an ISO datetime string into a datetime object. If no timezone information is given it's assumed to be local"""
	dt = dateutil.parser.parse(isostring)
	if dt.tzinfo == None: # if it's a naive datetime
		dt = dt.replace(tzinfo=tzlocal())
	return dt
