import datetime, pytz
from pprint import pprint
from timeseries.helpers import series_filter, live_filter

f = {'HVAC' : {'VRF' : { 'series' : { 'Name' : ['Mezzanine', 'Control Room'] }, 'columns' : ['SetTemp', 'InletTemp']}},
	'Electric' : {'Circuits' : { 'series' : { 'Channel' : ['Channel #1'] }, 'columns' : ['Current', 'Energy']}}}
pprint(f)

# now = pytz.UTC.localize(datetime.datetime.utcnow())
# earlier = now - datetime.timedelta(days=2)

print "\n============================\n"

# pprint(series_filter(f, earlier, now))

pprint(live_filter(f))