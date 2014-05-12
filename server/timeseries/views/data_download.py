import csv
import json
import timeseries.helpers as h
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseServerError
from commonssite.settings import datetime_out_format

def makedownload(request):
	return render(request, 'timeseries/download.html', {'systems' : h.systems_dict()})

def download_csv(request):
	# parse start and end times
	try:
		tstart = h.parse_time(request.GET.get('tstart'))
	except Exception as e:
		print "download_csv tstart error: ", e
		return HttpResponseServerError("To download data, a start time must be specified")
	try:
		tend = h.parse_time(request.GET.get('tend'))
	except Exception as e:
		print "download_csv tend error: ", e
		return HttpResponseServerError("To download data, an end time must be specified")
	try:
		series = json.loads(request.GET.get('series'))
	except Exception as e:
		print "download_csv series error: ", e
		return HttpResponseServerError("To download data, a series must be specified")
	objects = h.series_filter(series, tstart, tend)
	if len(objects) > 0:
		# set up the CSV writer
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="commonsdata.csv"'
		writer = csv.writer(response)

		csv_headers = set(['Time']) # a set only keeps unique values
		for obj in objects:
			csv_headers |= set(obj['H'].keys()) # this behaves like list.extend, but since it's a set it doesn't allow duplicates
			csv_headers |= set(obj['D'].keys())
		csv_headers = list(csv_headers) # convert from set back to list
		# make sure 'Time' is the first row
		csv_headers.pop(csv_headers.index('Time'))
		csv_headers.insert(0, 'Time')
		# first row of the CSV is csv_headers
		writer.writerow(csv_headers)

		# helper to get index of column header
		def col(name):
			return csv_headers.index(name)

		tindex = col('Time')
		# loop over all rows of queried data and write them
		for obj in objects:
			row = [None] * len(csv_headers) # begin with a blank row
			for k, v in obj['H'].iteritems():
				row[col(k)] = v
			for k, v in obj['D'].iteritems():
				row[col(k)] = v
			row[tindex] = obj['Time'].strftime(datetime_out_format)
			writer.writerow(row)
		return response
	else:
		return HttpResponseServerError("unable to process series specification")