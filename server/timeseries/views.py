from django.http import HttpResponse
from django.shortcuts import render
from hvac.models import ErvEntry, VrfEntry
from electric.models import ChannelEntry, DeviceSummary
from solar.models import SMAOverview, SMAPanels, SMAWeather
import csv, datetime, pytz
from commonssite.settings import datetime_out_format

# Create your views here.
def index(request):
	return render(request, 'timeseries/download.html', {})

def __date_parse(datestring_arg):
	# ISO 8601 specifies a universal datetime format as yyyyMMddTHHmmssZ
	datestring_arg = ''.join(datestring_arg.split('T'))
	fmt = r'%Y%m%d%H%M%S'
	unaware = datetime.datetime.strptime(datestring_arg, fmt)
	dt_with_timezone = pytz.UTC.localize(unaware)
	return dt_with_timezone

def __data_range(request, cls, tstart, tend):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="commonsdata.csv"'
	writer = csv.writer(response)

	headers = cls.all_headers()
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

def generic_csv(request, model):
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
	return __data_range(request, model, tstart, tend)

def vrf_csv(request):
	return generic_csv(request, VrfEntry)
	

def erv_csv(request):
	return generic_csv(request, ErvEntry)

def channel_csv(request):
	return generic_csv(request, ChannelEntry)

def elec_summary_csv(request):
	return generic_csv(request, DeviceSummary)

def solar_power_csv(request):
	return generic_csv(request, SMAPanels)

def solar_weather_csv(request):
	return generic_csv(request, SMAWeather)

def solar_overview_csv(request):
	return generic_csv(request, SMAOverview)
