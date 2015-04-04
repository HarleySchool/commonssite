#!/usr/bin/python
#
# NOTE: this is just a lightweight wrapper around the logging functions and is temporary.
# We *should* install and use cron so that crashes in the loggers don't halt data collection
from django.core.management import call_command
import time
from sys import argv, exit

last_run = 0
target_run = -1
interval = 30 # default to 30 seconds
sequential_errors = 0

if '--interval' in argv and len(argv) > argv.index('--interval'):
	interval = int(argv[argv.index('--interval')+1])

while True:
	time_to_target = target_run - time.time()
	if time_to_target > 0:
		time.sleep(time_to_target)
	elif time_to_target < -5:
		print "WARNING: running behind by %d seconds!" % time_to_target
		interval = interval + 1
	# run logging command
	try:
		start_time = time.time()
		call_command("log_now")
		target_run = start_time + interval
		sequential_errors = 0
	except KeyboardInterrupt:
		choice = raw_input("cancel logging? [y/N] ")
		if choice[0] in "yY":
			break
	except Exception as e:
		print "Logging Error: '%s'" % e
		target_run = start_time + 10
		sequential_errors = sequential_errors + 1
		if sequential_errors > 10:
			print "Too many errors. exiting!"
			exit(1)
