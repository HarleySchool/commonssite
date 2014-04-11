from django.shortcuts import render
import timeseries.helpers as h

def makechart(request):
	return render(request, "timeseries/makechart.html", {'systems' : h.systems_dict()})

def live(request):
	return render(request, 'timeseries/live.html', {'systems' : h.systems_dict()})