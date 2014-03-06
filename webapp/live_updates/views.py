from django.shortcuts import render
from commonssite.miscellaneous import VerisMonitor

# Create your views here.
def updates(request):
	m = request.session.get('monitor', None)
	if not m:
		m = VerisMonitor()
		request.session['monitor'] = m
	return render(request, 'live_updates/veris_tables.html', {'monitor' : m.get_new_data()})
