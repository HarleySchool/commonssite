# This script will fix all improperly-timezoned UTC objects
#
# WARNING: THIS SCRIPT IS RUN INDISCRIMINANTLY ON ALL OBJECTS IN THE REGISTRY. RUNNING IT TWICE
# WILL REINTRODUCE 4-HOUR-OFF ERRORS!!
#
# The problem is that pytz.UTC.localize(datetime.datetime.now()) will take the _local time_ and
# mark it as UTC-time (it will be 4 hours slow). This is how the scrapers have been working
# until 4/9/14.
from datetime import datetime, timedelta
import pytz

from timeseries import get_registered_model 
from timeseries.models import ModelRegistry

# On Mar 09, 2014, the clock changed from 01:59 to 03:00. 2:30am never happened.
# So, any date less than 2:30 is pre-jump and any date greater than 2:30 is post-jump
DST = pytz.UTC.localize(datetime(2014, 3, 9, 2, 30)) # divider between DST and non-DST
FIX = pytz.UTC.localize(datetime(2014, 4, 10, 12, 30)) # date that the code was fixed to utcnow() (and no update is needed)

plus4 = timedelta(hours=4)
plus5 = timedelta(hours=5)

for registry in ModelRegistry.objects.all():
	model = get_registered_model(registry.model_class)
	print "updating entries for", model.__name__
	for entry in model.objects.all():
		print entry.id
		if entry.Time < FIX:
			if entry.Time < DST:
				entry.Time += plus5
			else:
				entry.Time += plus4
			entry.save()
