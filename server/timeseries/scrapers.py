import time
import operator
import datetime
import pytz
from timeseries import helpers as h

class ScraperBase(object):
	"""A scraper base class which takes care of shared functionality

	The old scraping method worked by keeping a schedule of tasks and executing a scraper every 20 minutes or so.
	This version works by logging new data as frequently as possible (tagged with temporary=True), and then later
	using compute_average_of_temporaries() to save data points permanently.
	"""

	def __init__(self, model_class, registry_instance):
		self._model = model_class
		self._registry = registry_instance

	def compute_average_of_temporaries(self):
		"""Take an average or mode of all measurements (since the last permanent one) and save it.
		"""
		last_permanent = self._model.objects.filter(temporary=False).last()
		# if this has never been run, last_permanent will be None
		last_permanent_time = last_permanent.Time if last_permanent else pytz.UTC.localize(datetime.datetime(1970,1,1))
		# make a queryset for all the objects that will go into our computation
		data_points = self._model.objects.filter(temporary=True, Time__gt=last_permanent_time).order_by('Time')
		# first, separate the big queryset of points into multiple smaller lists based on their index
		indexed_objects = h.split_on_indexes(data_points)
		# there will be one new averaged object inserted per index
		for index, objects in indexed_objects.iteritems():
			if len(objects) == 0:
				continue
			elif len(objects) == 1:
				# edge-case: average is broken if there is only 1 object.
				objects[0].temporary = False
				objects[0].save()
				continue
			# adding timedelta here is a hack to prevent collisions with duplicate times
			tend = objects[-1].Time + datetime.timedelta(seconds=1)
			# we will construct the object from a kwarg dict
			kwargs = {'temporary' : False, 'Time' : tend}
			# numeric types are averaged; all others are plurality vote
			# note that the interval is NOT assumed to be regular; votes and averages are weighted by the span of
			# time between any two measurements
			# running average is computed using the formula for the area of a trapezoid (we assume that a linear fit between points is good enough)
			prev_point = vars(objects[0]) # the 'previous' value in the loop
			total_span = 0.0
			value_fields = [(f.get_attname(), f.get_internal_type(), f.null) for f in self._model._meta.fields if f.get_attname() in self._model.get_field_names()]
			# model_average is a map from attributes => (current average or votes)
			# initialize averages according to the 0th object
			model_average = dict([(nm, 0.0 if typ in h.model_types['numeric'] and not isnull else {prev_point[nm] : 1}) for nm, typ, isnull in value_fields])
			for curr_point in objects[1:]:
				span_seconds = h.timedelta_seconds(curr_point.Time - prev_point['Time'])
				total_span += span_seconds
				for nm, typ, isnull in value_fields:
					val = vars(curr_point)[nm]
					prev_val = prev_point[nm]
					# NUMERIC NON-NULL TYPES: running average
					if typ in h.model_types['numeric'] and not isnull:
						if prev_val != None:
							mean_in_span = (val + prev_val) / 2.0
							model_average[nm] += (mean_in_span - model_average[nm]) * span_seconds / total_span
					# ALL OTHER TYPES: plurality vote
					else:
						# count occurances of val by mapping val:count
						# but count is actually span_seconds so that values with longer spans get more votes
						model_average[nm][val] = model_average[nm].get(val, 0) + span_seconds
				prev_point = vars(curr_point)
			# at this point, all numeric types are averaged and all non-numeric types have a vote tally.
			# now we must get the plurality winners for non-numeric types. Results are put into kwargs.
			for nm, typ, isnull in value_fields:
				if typ in h.model_types['numeric'] and not isnull:
					kwargs[nm] = model_average[nm]
				elif len(model_average[nm]) > 0:
					# http://stackoverflow.com/a/268285/1935085
					# get value with most votes
					kwargs[nm] = max(model_average[nm].iteritems(), key=operator.itemgetter(1))[0]
				else:
					kwargs[nm] = None
			# lastly we need to add the index columns back in
			typical_object = objects[-1] # really any of them will work here
			index_field = typical_object.get_index_column()
			if index_field:
				kwargs.update({index_field: vars(typical_object)[index_field]})
			# create and save the new object
			new_object = self._model(**kwargs)
			new_object.save()
		self._model.remove_expired()

	def status_ok(self):
		self._registry.status = 0

	def status_format_error(self):
		self._registry.status = 1

	def status_comm_error(self):
		self._registry.status = 2

	def get_and_save_single(self):
		try:
			for new_data in self.get_data():
				new_data.temporary = True
				new_data.save(force_insert=True)
			print '=================='
			print '%s done at %s' % (self.__class__.__name__, time.time())
		except Exception as e:
			print "Scraper error that wasn't caught by subclass!"
			print e
			self.status_comm_error()
		finally:
			self._registry.save() # update status in the database

	def get_data(self):
		"""Return a list of TimeseriesBase (subclass) models. get_data must be implemented by subclasses of ScraperBase
		"""
		self.status_comm_error()
		return []
