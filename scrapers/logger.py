# top-level logging script
import time, datetime, math
from threading import Thread
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
			updates = self.scraper.get_data()
			print "------------------------\n%s\tgetting log at" % self.scraper.__class__.__name__, now, ": %d UPDATES" % len(updates)
			for entry in updates:
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
				print "%s\tnext log scheduled for" % self.scraper.__class__.__name__, datetime.datetime.fromtimestamp(tnext)
			except KeyboardInterrupt:
				print "exiting logger thread"
				break
			except Exception as e:
				print "error, but continuing:", type(e)
				print e

if __name__ == '__main__':
	ervlog = Logger(ScraperERV(), 20*MINUTE) # log every 20 minutes forever 
	ervlog.start()
	vrflog = Logger(ScraperVRF(), 20*MINUTE) # log every 20 minutes forever 
	vrflog.start()
	veris_circuits_log = Logger(ScraperCircuits(), 20*MINUTE) # log every 20 minutes forever 
	veris_circuits_log.start()
	veris_summary_log = Logger(ScraperPowerSummary(), 20*MINUTE) # log every 20 minutes forever 
	veris_summary_log.start()
	solar_panel_log = Logger(ScraperSolarPanels(), 20*MINUTE)
	solar_panel_log.start()
	solar_weather_log = Logger(ScraperSolarWeather(), 20*MINUTE)
	solar_weather_log.start()
	solar_overview_log = Logger(ScraperSolarOverview(), 20*MINUTE)
	solar_overview_log.start()

	try:
		ervlog.join()
		vrflog.join()
		veris_circuits_log.join()
		veris_summary_log.join()
		smalog.join()
		solar_panel_log.join()
		solar_weather_log.join()
		solar_overview_log.join()
	except Exception as e:
		print "somthing went wrong with join...?"
		print e
	print "--main done--"
