import csv
import datetime
import timeseries.helpers as h
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from commonssite.settings import datetime_out_format
from timeseries.models import ModelRegistry

def index(request):
	return render(request, 'timeseries/download.html', {'systems' : h.systems_dict()})

def __csv_range(request, cls, tstart, tend):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="%s.csv"' % cls.__name__
	writer = csv.writer(response)

	headers = cls.get_header_names() + cls.get_field_names()
	writer.writerow(headers)

	q = cls.objects.filter(Time__gte=tstart, Time__lt=tend)

	# loop over all rows of queried data and write them
	for obj in q:
		csv_row = map(lambda h: obj.__dict__.get(h, ''), headers)
		# special formatting for datetime so it's readable by spreadsheet programs
		tspot = headers.index('Time')
		if tspot > -1:
			csv_row[tspot] = csv_row[tspot].strftime(datetime_out_format)
		writer.writerow(csv_row)
	return response

def generic_csv(request, model_name):
	try:
		tstart = h.parse_time(request.GET.get('tstart'))
	except Exception as e:
		print e
		tstart = datetime.datetime.utcfromtimestamp(0) # default to beginning of time
	try:
		tend = h.parse_time(request.GET.get('tend'))
	except Exception as e:
		print e
		tend = datetime.datetime.utcnow() # default to now
	# find the specified model class
	m = ModelRegistry.objects.get(short_name=model_name)
	# retrieve model class from cache, or import it
	try:
		return __csv_range(request, h.get_registered_model(m.model_class), tstart, tend)
	except ImportError:
		return HttpResponseServerError("Could not locate database table for type %s" % model_name)