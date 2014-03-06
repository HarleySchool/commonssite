from django.shortcuts import render
from commonssite.miscellaneous.veris_monitor import Monitor

# Create your views here.
def updates(request):
	m = request.session.get('monitor', None)
	if not m:
		m = Monitor()
	else:
		m = (Monitor()).from_dicts(m)
	updates = m.get_new_data()
	request.session['monitor'] = m.as_dicts()
	return render(request, 'live_updates/update_table.html', {'monitor' : updates})
