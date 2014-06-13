import csv
import json
import timeseries.helpers as h
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from functools import partial
from django.shortcuts import render, redirect
from timeseries.models import Series
from commonssite.settings import datetime_out_format

def analyze(request):
	return render(request, 'timeseries/analyze.html', {'systems' : h.systems_schema()})

def download_csv(request):
	# parse start and end times
	try:
		tstart = h.parse_time(request.GET.get('tstart'))
	except Exception as e:
		print "download_csv tstart error: ", e
		return HttpResponseBadRequest("To download data, a start time must be specified")
	try:
		tend = h.parse_time(request.GET.get('tend'))
	except Exception as e:
		print "download_csv tend error: ", e
		return HttpResponseBadRequest("To download data, an end time must be specified")
	try:
		series = json.loads(request.GET.get('series'))
		print series
	except Exception as e:
		print "download_csv series error: ", e
		return HttpResponseBadRequest("To download data, a series must be specified")
	
	# use helper file to fetch and format data
	serieses = h.series_filter(series, tstart, tend, dateformat=datetime_out_format)
	
	# set up the CSV writer
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="commonsdata.csv"'
	writer = csv.writer(response)

	def qualify_header(index, col_name):
		if index:
			return '%s %s' % (str(index), col_name)
		else:
			return col_name

	csv_headers = ['Time']
	for series in serieses:
		if len(series['data']) > 0:
			columns = series['data'][0].keys()
			if 'Time' in columns: columns.remove('Time')
			# map the qualify_header function onto the columns for this series
			csv_headers.extend(map(partial(qualify_header, series['index']), columns))
	# first row of the CSV is csv_headers
	writer.writerow(csv_headers)
	n_csv_columns = len(csv_headers)

	# helper to get index of column header
	def col(name):
		return csv_headers.index(name)

	# we will loop over all rows of queried data and write them in order of increasing Time.
	# since objects are split across different indexes, we need to do some book-keeping
	# so that we always get the chronologically next object
	next_indexes = [0] * len(serieses) # next un-used data point in each series
	series_lengths = [len(s['data']) for s in serieses] # size of each series

	# helper function to get the chronologically next un-used object
	def next_object():
		min_object = None
		min_series = -1
		for i, s in enumerate(serieses):
			# if this series still has un-used data points..
			if next_indexes[i] < series_lengths[i]:
				# if this series' next point is the closest yet..
				if min_object is None or s['data'][next_indexes[i]]['Time'] < min_object['Time']:
					min_object = s['data'][next_indexes[i]]
					min_series = i
		next_indexes[min_series] += 1
		return serieses[min_series]['index'], min_object

	# because multiple series may actually share the same timestamp, we hold off on writing the row until a new timestamp shows up
	building_row = [None] * n_csv_columns
	# loop until 'next_indexes' has caught up with 'series_lengths'
	while sum([next_indexes[i] < series_lengths[i] for i in range(len(serieses))]):
		index, obj = next_object()
		# check if we're on to a new timestamp. if so, write the previous row and start a new one
		if obj['Time'] != building_row[0] and building_row[0] is not None:
			# new timestamp. write the previous row
			writer.writerow(building_row)
			building_row = [None] * n_csv_columns
		building_row[0] = obj['Time']
		for name, value in obj.iteritems():
			if name == 'Time' : continue
			building_row[col(qualify_header(index, name))] = value
	# write the final row
	writer.writerow(building_row)
	return response
