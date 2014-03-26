from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from hvac.models import ErvEntry, VrfEntry
from electric.models import ChannelEntry, DeviceSummary
from solar.models import SMAOverview, SMAPanels, SMAWeather
import csv
import datetime
import pytz
import json
from commonssite.settings import datetime_spreadsheet_format

# Create your views here.
def index(request):
	return render(request, 'timeseries/download.html', {})

@csrf_exempt
def chart(request):
	return render(request, 'timeseries/charttest.html', {})

def __data_range(request, cls, tstart, tend, format='csv', cols=[], datefmt=datetime_spreadsheet_format, collapse_unique=True):
	if format is 'csv':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="commonsdata.csv"'
		writer = csv.writer(response)
	elif format is 'json':
		series = {}
		response = HttpResponse(content_type='application/json')

	# get column headers
	simple_headers = cols or cls.all_headers() # column headers with simple name->value map
	if 'Time' not in simple_headers:
		simple_headers.insert(0, 'Time')
	headers = [h for h in simple_headers] # all column headers (including collapsed)
	# collapse together the 'unique_together' columns into one (keep time separate)
	if collapse_unique:
		try:
			unq_headers = list(cls._meta.unique_together[0])
			unq_headers.remove('Time') # leave time to its own column
			for h in unq_headers:
				if h in simple_headers:
					simple_headers.remove(h)
				if h in headers:
					headers.remove(h)
			collapse_column = '.'.join(unq_headers)
			headers.insert(1, collapse_column)
		except Exception as e:
			collapse_unique = False
			simple_headers = cols or cls.all_headers()
			print "collapse failed:", e

	if format is 'csv':
		writer.writerow(headers)
	elif format is 'json':
		for h in headers:
			series.update({h : []})

	q = cls.objects.filter(Time__gte=tstart, Time__lt=tend)

	# loop over all rows of queried data and write them
	for obj in q:
		value_list = map(lambda h: obj.__dict__.get(h, ''), simple_headers)
		# collapse 'unique-together' values together
		if collapse_unique:
			joint_val = '.'.join([str(val) for val in map(lambda h: obj.__dict__.get(h, ''), unq_headers)])
			value_list.insert(1, joint_val)
		# special formatting for datetime so it's readable by spreadsheet programs
		tspot = headers.index('Time')
		if tspot > -1 and datefmt:
			value_list[tspot] = value_list[tspot].strftime(datefmt)
		if format is 'csv':
			writer.writerow(value_list)
		elif format is 'json':
			for i in range(len(headers)):
				series[headers[i]].append(value_list[i])
	if format is 'json':
		response.write(series)
	return response

def request_data(request):
	if request.is_ajax() and request.method == 'POST':
		api_call = json.loads(request.read())
		# parse according to API
		tstart = float(api_call['start time']) / 1000
		tstart = datetime.datetime.utcfromtimestamp(tstart)
		tend   = float(api_call['end time']) / 1000
		tend = datetime.datetime.utcfromtimestamp(tend)
		is_daily = api_call.get('daily', {}).get('Enabled', False)
		time = datetime.strptime(api_call.get('daily', {}).get('time', '1200'), r'%H%M') if is_daily else None
		system = api_call.get('system', {})
		cols = system.get('cols', [])
		cls = None
		if system.get('name') == 'HVAC-ERV':
			cls = ErvEntry
		elif system.get('name') == 'HVAC-VRF':
			cls = VrfEntry
		elif system.get('name') == 'VERIS-CHANNELS':
			cls = ChannelEntry
		elif system.get('name') == 'VERIS-SUMMARY':
			cls = DeviceSummary
		elif system.get('name') == 'SOLAR-WEATHER':
			cls = SMAWeather
		elif system.get('name') == 'SOLAR-POWER':
			cls = SMAWeather
		elif system.get('name') == 'SOLAR-SUMMARY':
			cls = SMAOverview
		return __data_range(request, cls, tstart, tend, format='json', cols=cols)
	else:
		return HttpResponse(405)

def __date_parse(datestring_arg):
	# ISO 8601 specifies a universal datetime format as yyyyMMddTHHmmssZ
	datestring_arg = ''.join(datestring_arg.split('T'))
	fmt = r'%Y%m%d%H%M%S'
	unaware = datetime.datetime.strptime(datestring_arg, fmt)
	dt_with_timezone = pytz.UTC.localize(unaware)
	return dt_with_timezone

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
