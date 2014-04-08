# Imports!
import time
import threading
import heapq
from commonssite.server.timeseries.models import ModelRegistry
from commonssite.server.timeseries import get_registered_scraper

# Converts seconds to minutes
def minutes(seconds):
	# because math
	return seconds * 60

class scheduler():
# Main Scheduler class
	def __init__(self):
		self.heap = []
		self.taskdict = {}
	def register(self, func, interval):
		# Registers Functions into a dict
		self.taskdict[func] = interval
	def run_threaded(self, func):
		# To run Functions threaded
		job_thread = threading.Thread(target=func)
		job_thread.start()
	def popandnext(self):
		# Pops the next function off the list and computes the next go time
		nextgo, func = heapq.heappop(self.heap)
		nnextgo = nextgo + self.taskdict[func]
		heapq.heappush(self.heap, (nnextgo, func))
		nexttime = self.heap[0][0]
		return [func, nexttime]
	def startheap(self):
		# Initializes the heap
		# All function run on startup
		t = time.time()
		for func, interval in self.taskdict.iteritems():
			nextgo = t
			heapq.heappush(self.heap, (nextgo, func))
	def main(self):
		# main loop
		self.startheap()
		while True:
			## Insert thing to do here ##
			# should not take over the time speced in interval
			# don't even cut it close
			# use run_theaded to clear the main thread
			#############################
			print '=================='
			func, nexttime = self.popandnext()
			self.run_threaded(func)
			# Calculate the time that we should sleep
			sleeptime = nexttime - time.time()
			# Print some things
			print "I done did it at %s, I'm gon do it again in %s seconds" % (time.time(), sleeptime)
			# Gets around a negative sleep time error by using pass
			if sleeptime < 1 and sleeptime > -3:
				pass
			elif sleeptime < -3:
				print 'Sleep time error, heave you suspended your computer recently?'
				exit()
			else:
				# If there is more than 1 second between functions, sleep the remainder of the time
				time.sleep(sleeptime)

def dolog(scraper):
	# Returns a function that logs data in the database
	def getandsave():
		data = scraper.get_data()
		for item in data:
			item.save(force_insert=True)
	return getandsave

if __name__ == '__main__':
	cron = scheduler()
	# Get a list of scrapers
	model_list = [get_registered_scraper(r.scraper_class) for r in ModelRegistry.objects.all()]
	for scraper in model_list:
		# Initialize all of them
		scraperinst = scraper()
		# Register with the scheduler
		cron.register(dolog(scraperinst), 20)
	# Run the Scheduler (forever)
	cron.main()
