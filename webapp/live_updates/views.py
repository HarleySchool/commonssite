from django.shortcuts import render
from commonssite.miscellaneous import VerisMonitor

# Create your views here.
def initial(request):
	# create monitor object fresh. stored in session for updates.
	m = VerisMonitor()
	init_vals = m.get_new_data() # initial get-data call sets baseline values
	request.session['monitor'] = m.serialize()
	settings = (m.get_thresholds(), m.get_ignored())
	return render(request, 'live_updates/monitor_wrapper.html', {'monitor' : init_vals, 'settings' : settings})

def update(request):
	m = request.session.get('monitor', None)
	if not m:
		m = VerisMonitor()
	else:
		m = VerisMonitor.deserialize(m)
	m.get_new_data()
	request.session['monitor'] = m.serialize()
	settings = (m.get_thresholds(), m.get_ignored())
	return render(request, 'live_updates/veris_tables.html', {'monitor' : m.get_old_data(), 'settings' : settings})

def config(request):
	# get monitor from session
	m = request.session.get('monitor', None)
	if not m:
		m = VerisMonitor()
	else:
		m = VerisMonitor.deserialize(m)
	# update threshold values
	for k,v in m.get_thresholds().items():
		m.set_thresh(k, float(request.GET.get(k, v)))
	# update ignored values
	print "IGNORE", request.GET.get("ignore")
	m.set_ignored(request.GET.get("ignore", m.get_ignored()))
	# return rendered inner-page (just tables)
	request.session['monitor'] = m.serialize()
	settings = (m.get_thresholds(), m.get_ignored())
	return render(request, 'live_updates/veris_tables.html', {'monitor' : m.get_old_data(), 'settings' : settings})

