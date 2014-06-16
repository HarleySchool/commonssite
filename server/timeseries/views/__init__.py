import json
from data_api import systems, series, single, save_series, load_series
from data_analysis import download_csv, analyze
from admin_pages import status
import timeseries.helpers as h
from timeseries.models import Live
from django.shortcuts import render

def live(request):
	charts_table = {}
	for chart in Live.objects.all():
		col = chart.location % 2
		row = chart.location / 2
		charts_table['%d%d' % (row,col)] = {
			'location' : chart.location,
			'rowspan' : chart.rowspan,
			'colspan' : chart.colspan,
			'title' : chart.title,
			'series' : json.dumps(chart.series.spec)
		}
	return render(request, 'timeseries/live.html', {'charts_table' : charts_table})
