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

	def compute_average_of_temporaries(self, interval=1200):
		"""Take an average or mode of all measurements (since the last permanent one) and save it.

		If interval is given (default 1200sec) then averages are computed over intervals of that length
		"""
		last_permanent = max(self._model.objects.filter(temporary=False).last(), self._model.objects.filter(temporary=True).order_by('Time')[0])
		# if this has never been run, last_permanent will be None
		last_permanent_time = last_permanent.Time if last_permanent else pytz.UTC.localize(datetime.datetime(1970,1,1))

		UTC_now = pytz.UTC.localize(datetime.datetime.utcnow())

		if not interval:
			interval = UTC_now - last_permanent_time
		elif type(interval) is int:
			interval = datetime.timedelta(seconds=interval)

		interval_end = last_permanent_time + interval
		i = 1
		while interval_end <= UTC_now:
			if i > 1: print "[%s] getting more intervals since" % (self.__class__.__name__), last_permanent_time
			i += 1
			# make a queryset for all the objects that will go into our computation
			data_points = self._model.objects.filter(
				temporary=True,
				Time__gte =last_permanent_time,
				Time__lte=interval_end).order_by('Time')
			# first, separate the big queryset of points into multiple smaller lists based on their index
			indexed_objects = h.split_on_indexes(data_points)
			# there will be one new averaged object inserted per index
			for index_tuple, objects in indexed_objects.iteritems():
				if len(objects) == 0:
					continue
				# adding timedelta here is a hack to prevent collisions with duplicate times
				tend = objects[-1]['Time'] + datetime.timedelta(seconds=1)
				# we will construct the object from a kwarg dict
				kwargs = {'temporary' : False, 'Time' : tend}
				# set the index value for this group of objects
				index_col = self._model.get_index_column()
				if index_col: kwargs[index_col+'_id'] = index_tuple[0]
				perm_obj, created = self._model.objects.get_or_create(**kwargs)
				# numeric types are averaged (see note below); all others are plurality vote
				# note that the interval is NOT assumed to be regular; votes and averages are weighted by the span of
				# time between any two measurements
				# running average is computed using the formula for the area of a trapezoid (we assume that a linear fit between points is good enough)
				#
				# NOTE about numeric averages: if the model allows for null values, we need to be careful not to do arithmetic on `None`, but rather
				# wait patiently for the next not-None value, which requires storing the time of the last value _separately for each attribute_

				# value_fields is a list of tuples of (model attribute, type of attribute)
				value_fields = [(f.get_attname(), f.get_internal_type()) for f in self._model._meta.fields if f.get_attname() in self._model.get_field_names()]

				# model_average is a map from attributes => (current average or votes)
				# with initial values according to the 0th object in our list of objects
				model_average = dict([(nm, None if typ in h.model_types['numeric'] else {}) for nm, typ in value_fields])

				# get an average for each field
				for nm, typ in value_fields:
					# numeric types: simple average.
					# non-numeric types: dictionary mapping values to vote counts
					num = typ in h.model_types['numeric']
					running_avg = None if num else {}
					total_time = 0.0
					last_valid_point = None

					for data_point in objects:
						val = data_point[nm]
						if val is not None:
							# got valid data.. check if it's the first oen
							if last_valid_point is None:
								# this is the first valid point
								if num:
									running_avg = val
								else:
									# somewhat arbitrary choice that first point gets 1-second of weight
									running_avg[val] = 1

							else:
								# there is a valid data point before this one
								span_seconds = h.timedelta_seconds(data_point['Time'] - last_valid_point['Time'])
								total_time += span_seconds
								# weight this point based on time elapsed since last point
								if num:
									if total_time == 0: continue
									# count trapezoidal area
									mean_in_span = (val + last_valid_point[nm]) / 2.0
									running_avg += (mean_in_span - running_avg) * span_seconds / total_time
								else:
									# each elapsed seconds counts as 1 vote
									running_avg[val] = running_avg.get(val, 0) + span_seconds
							last_valid_point = data_point
						else:
							# data invalid.. no update
							continue

					model_average[nm] = running_avg

				# at this point, all numeric types are averaged and all non-numeric types have a vote tally.
				# now we must get the plurality winners for non-numeric types. Results are put into kwargs.
				for nm, typ in value_fields:
					if typ in h.model_types['numeric']:
						kwargs[nm] = model_average[nm]
					elif len(model_average[nm]) > 0:
						# http://stackoverflow.com/a/268285/1935085
						# get value with most votes
						kwargs[nm] = max(model_average[nm].iteritems(), key=operator.itemgetter(1))[0]
					else:
						kwargs[nm] = None
				# update and save the object (creating or overwriting)
				try:
					for k,v in kwargs.iteritems():
						setattr(perm_obj, k, v)
					perm_obj.save()
				except Exception as e:
					print "Error getting average for [%s] over" % self.__class__.__name__, last_permanent_time, interval_end
					print "\t", e
			last_permanent_time = interval_end
			interval_end = last_permanent_time + interval
		self._model.remove_expired()

	def status_ok(self):
		self._registry.status = 0

	def status_format_error(self):
		self._registry.status = 1

	def status_comm_error(self):
		self._registry.status = 2

	def get_and_save_single(self):
		try:
			tstart = time.time()
			data = self.get_data()
			print "[%s] got new data in %0.3f seconds" % (self.__class__.__name__, time.time() - tstart)
			for new_data in data:
				new_data.temporary = True
				new_data.save(force_insert=True)
		except Exception as e:
			print "Scraper error that wasn't caught by subclass [%s]" % self.__class__.__name__
			print e
			self.status_comm_error()
		finally:
			self._registry.save() # update status in the database

	def get_data(self):
		"""Return a list of TimeseriesBase (subclass) models. get_data must be implemented by subclasses of ScraperBase
		"""
		self.status_comm_error()
		return []
