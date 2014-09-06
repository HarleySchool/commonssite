import timeseries.helpers as h
from django.shortcuts import render

def status(request):
	return render(request, "timeseries/status.html", )