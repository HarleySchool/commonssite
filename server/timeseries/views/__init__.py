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
		row, col = divmod(chart.location, 2)
		charts_table['%d%d' % (row,col)] = {
			'location' : chart.location,
			'bootstrap_colspan' : chart.colspan * 6,
			'title' : chart.title,
			'series' : json.dumps(chart.series.spec)
		}
	if '00' in charts_table and charts_table['00']['bootstrap_colspan'] == 12 and '01' in charts_table:
		del charts_table['01']
	elif '01' in charts_table and charts_table['01']['bootstrap_colspan'] == 12 and '00' in charts_table:
		del charts_table['00']

	if '10' in charts_table and charts_table['10']['bootstrap_colspan'] == 12 and '11' in charts_table:
		del charts_table['11']
	elif '11' in charts_table and charts_table['11']['bootstrap_colspan'] == 12 and '10' in charts_table:
		del charts_table['10']
	
	return render(request, 'timeseries/live.html', {'charts_table' : charts_table})
