import datetime, pytz
from pprint import pprint
from timeseries.helpers import system_filter, live_filter

f = [{'HVAC' : {'VRF' : { 'filter' : { 'Name' : ['Mezzanine', 'Control Room'] }, 'columns' : ['SetTemp', 'InletTemp']}}}, {'Electric' : {'Circuits' : { 'filter' : { 'Channel' : ['Channel #1'] }, 'columns' : ['Current', 'Energy']}}}]
pprint(f)

# now = pytz.UTC.localize(datetime.datetime.utcnow())
# earlier = now - datetime.timedelta(days=2)

print "\n============================\n"

# pprint(system_filter(f, earlier, now))

pprint(live_filter(f))