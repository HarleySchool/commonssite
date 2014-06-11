from data_api import systems, series, single, save_series, load_series
from data_download import download_csv
from data_charts import live
from admin_pages import status

from django.shortcuts import render, redirect
import timeseries.helpers as h
from timeseries.models import Series

def live(request):
	return render(request, 'timeseries/live.html', {'systems' : h.systems_schema()})

def analyze(request, series_id=None):
	preload_series = None
	if series_id:
		try:
			preload_series = Series.objects.get(string_hash=series_id)
		except:
			# attempted lookup of series failed. redirect to blank.
			return redirect('/data/analyze/')
	return render(request, 'timeseries/analyze.html', {'systems' : h.systems_schema(), 'preload_series' : preload_series.spec if preload_series else None})