# top-level logging script
import time, datetime, math
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
		tnext = tstart
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

		# wait for next one
		while self.span < 0 or tnext < tend:
			try:
				now = sleep_remainder()
				do_log()
				# update tnext to be the next integer multiple of 'interval' seconds
				tnext = tstart + self.interval * (1 + math.floor((now - tstart) / self.interval))
				print "next log scheduled for", datetime.datetime.fromtimestamp(tnext)
			except KeyboardInterrupt:
				print "exiting HVAC logger thread"
				break
			except Exception as e:
				print "error, but continuing:", type(e)
				print e

if __name__ == '__main__':
	hvlog = Logger(ScraperHvac(), 20*MINUTE) # log every 20 minutes forever 
	hvlog.start()
	verlog = Logger(ScraperElectric(), 20*MINUTE) # log every 20 minutes forever 
	verlog.start()

	hvlog.join()
	print "--main done--"
