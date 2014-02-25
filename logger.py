# top-level logging script
import time, datetime
from threading import Thread
from commonssite.settings import hvac_log_interval
from commonssite.scrapers import *

MINUTE = 60
HOUR = 60*MINUTE
DAY = 24*HOUR
WEEK = 7*DAY

class HvacLogger(Thread):

	def __init__(self, loginterval, logspan=-1):
		self.scraper = ScraperHvac()
		self.interval = loginterval
		self.span = logspan

	def run(self):
		"""start logging in the background

		this function is executed in a separate thread when obj.start() is called"""
		tstart = time.time()
		tnext = tstart + self.interval
		tend = tstart + self.span

		def do_log():
			now = datetime.datetime.now()
			print "getting log at", now
			for entry in self.scraper.get_data():
				entry.save(force_insert=True)

		def sleep_remainder():
			now = time.time()
			tleft = max(0, tnext-now)
			time.sleep(tleft)

		# execution begins with a log entry
		do_log()
		# now wait for next one
		while self.span < 0 or tnext < tend:
			try:
				sleep_remainder()
				do_log()
			except KeyboardInterrupt:
				print "exiting HVAC logger thread"
				break
			except Exception as e:
				print "error, but continuing:"
				print e

if __name__ == '__main__':
	hvlog = HvacLogger(10*MINUTE, 2*DAY) # log every 10 minutes for 2 days
	hvlog.start()

	hvlog.join()
	print "--main done--"
