from data_api import systems, series, single, save_series, load_series
from data_analysis import download_csv, analyze
from admin_pages import status
import timeseries.helpers as h
from django.shortcuts import render

def live(request):
	return render(request, 'timeseries/live.html', {'systems' : h.systems_schema()})
