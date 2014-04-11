import csv
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
		tstart = h.parse_time(request.GET.pop('tstart'))
	except Exception as e:
		print e
		return HttpResponseServerError("To download data, a start time must be specified")
	try:
		tend = h.parse_time(request.GET.pop('tend'))
	except Exception as e:
		print e
		return HttpResponseServerError("To download data, an end time must be specified")
	# get the QuerySets for the specified series (where the GET itself is treated as the filter object, and we don't allow multiple systems)
	qs = h.system_filter([request.GET])
	if len(qs) > 0:
		queryset = qs[0]
		# set up the CSV writer
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="%s.csv"' % queryset.model.__name__
		writer = csv.writer(response)

		# if columns were filtered (again, see timeseries.helpers.system_filter), then the result is not a QuerySet
		# but a ValuesQuerySet. A ValuesQuerySet has a '_fields' tuple of the relevant columns.
		if hasattr(queryset, '_fields'):
			headers = list(queryset._fields)
		# if it's a plain old QuerySet, then no columns were filtered and we use all of them, using the
		# get_header_names and get_field_names functions from timeseries.models.TimeseriesBase
		else:
			headers = queryset.model.get_header_names() + queryset.model.get_field_names()
		
		# first row of the CSV is headers
		writer.writerow(headers)

		# Finally filter by the time interval (note that the database STILL has not actually been queried)
		# Lazy queries are nice.
		queryset = queryset.filter(Time__gte=tstart, Time__lt=tend)

		# loop over all rows of queried data and write them
		# (HERE we actually hit the database)
		for obj in queryset:
			# construct the next row in the file by mapping "get value" onto the list of column headers
			# (note that map will preserve the order so that the columns stay lined up)
			csv_values_row = map(lambda h: obj.__dict__.get(h, ''), headers)
			# special formatting for datetime so it's readable by spreadsheet programs
			tspot = headers.index('Time')
			if tspot > -1:
				csv_values_row[tspot] = csv_values_row[tspot].strftime(datetime_out_format)
			writer.writerow(csv_values_row)
		return response
	else:
		return HttpResponseServerError("unable to process series specification")