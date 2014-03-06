from django.shortcuts import render
from commonssite.miscellaneous.veris_monitor import Monitor

# Create your views here.
def updates(request):
	m = request.session.get('monitor', None)
	if not m:
		request.session['monitor'] = Monitor()
	return render(request, 'live_updates/update_table.html', {'monitor' : m.get_new_data()})
