
model_cache = {}
def get_registered_model(class_path):
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
