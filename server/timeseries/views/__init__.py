from data_api import systems, series, single
from data_download import download_csv
from data_charts import live
from admin_pages import status

from django.shortcuts import render
import timeseries.helpers as h

def live(request):
	return render(request, 'timeseries/live.html', {'systems' : h.systems_schema()})

def analyze(request):
	return render(request, 'timeseries/analyze.html', {'systems' : h.systems_schema()})