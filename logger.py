# top-level logging script
import time, datetime
from threading import Thread
from commonssite.settings import hvac_log_interval
from commonssite.scrapers import *

MINUTE = 60
HOUR = 60*MINUTE
DAY = 24*HOUR
WEEK = 7*DAY

class Logger(Thread):

	def __init__(self, scraper_obj, loginterval, logspan=-1):
		Thread.__init__(self)
		self.scraper = scraper_obj
		self.interval = loginterval
		self.span = logspan

	def run(self):
		"""start logging in the background

		this function is executed in a separate thread when Logger.start() is called"""
		tstart = time.time()
		tnext = tstart + self.interval
		tend = tstart + self.span

		def do_log():
			now = datetime.datetime.now()
			print "------------------------\ngetting log at", now
			for entry in self.scraper.get_data():
				entry.save(force_insert=True)

		def sleep_remainder():
			now = time.time()
			tleft = max(0, tnext-now)
			time.sleep(tleft)
			return time.time()

		# execution begins with a log entry
		do_log()
		# now wait for next one
		while self.span < 0 or tnext < tend:
			try:
				now = sleep_remainder()
				do_log()
				# update tnext to be the next integer multiple of 'interval' seconds
				tnext = tstart + interval * (1 + math.floor((now - tstart) / interval))
				print "next log scheduled for", datetime.fromtimestamp(tnext)
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
