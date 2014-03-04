from django.http import HttpResponse
from django.shortcuts import render
from data.models import ErvEntry, VrfEntry
import csv, datetime, pytz

# Create your views here.
def index(request):
	return render(request, 'data/index.html', {})

def __date_parse(datestring_arg):
	# ISO 8601 specifies a universal datetime format as yyyyMMddTHHmmssZ
	datestring_arg = ''.join(datestring_arg.split('T'))
	fmt = r'%Y%m%d%H%M%S'
	unaware = datetime.datetime.strptime(datestring_arg, fmt)
	dt_with_timezone = pytz.UTC.localize(unaware)
	return dt_with_timezone

def __hvac_range(cls, request, tstart, tend):
	print "HVAC RANGE for", cls, "from", tstart, "to", tend
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="commonsdata.csv"'
	writer = csv.writer(response)

	headers = cls.all_headers()
	writer.writerow(headers)

	q = cls.objects.filter(Time__gte=tstart, Time__lt=tend)

	# loop over all rows of queried data and write them
	for vrf_obj in q:
		csv_row = map(lambda h: vrf_obj.__dict__.get(h, ''), headers)
		# special formatting for datetime so it's readable by spreadsheet programs
		tspot = headers.find('Time')
		if tspot > -1:
			csv_row[tspot] = csv_row[tspot].strftime('%Y-%m-%d %H:%M:%S')
		writer.writerow(csv_row)
	return response

def vrf_csv(request):
	try:
		tstart = __date_parse(request.GET.get('tstart'))
	except Exception as e:
		print e
		tstart = datetime.datetime.fromtimestamp(0)
	try:
		tend = __date_parse(request.GET.get('tend'))
	except Exception as e:
		print e
		tend = datetime.datetime.now()
	return __hvac_range(VrfEntry, request, tstart, tend)
	

def erv_csv(request):
	try:
		tstart = __date_parse(request.GET.get('tstart'))
	except Exception as e:
		print e
		tstart = datetime.datetime.fromtimestamp(0)
	try:
		tend = __date_parse(request.GET.get('tend'))
	except Exception as e:
		print e
		tend = datetime.datetime.now()
	return __hvac_range(ErvEntry, request, tstart, tend)