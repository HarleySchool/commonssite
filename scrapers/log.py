import time
import threading
import heapq
from commonssite.server.timeseries.models import ModelRegistry
from commonssite.server.timeseries import get_registered_scraper
def minutes(seconds):
	return seconds * 60
class scheduler():
	def __init__(self):
		self.heap = []
		self.taskdict = {}
	def register(self, func, interval):
		self.taskdict[func] = interval
	def run_threaded(self, func):
		job_thread = threading.Thread(target=func)
		job_thread.start()
	def popandnext(self):
		nextgo, func = heapq.heappop(self.heap)
		nnextgo = nextgo + self.taskdict[func]
		heapq.heappush(self.heap, (nnextgo, func))
		nexttime = self.heap[0][0]
		return [func, nexttime]
	def startheap(self):
		t = time.time()
		for func, interval in self.taskdict.iteritems():
			nextgo = t
			heapq.heappush(self.heap, (nextgo, func))
	def main(self):
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
			sleeptime = nexttime - time.time()
			print "I done did it at %s, I'm gon do it again in %s seconds" % (time.time(), sleeptime)
			if sleeptime < 1 and sleeptime > -3:
				pass
			elif sleeptime < -3:
				print 'Sleep time error, heave you suspended your computer recently?'
				exit()
			else:
				time.sleep(sleeptime)

def dolog(scraper):
	def getandsave():
		data = scraper.get_data()
		for item in data:
			item.save(force_insert=True)
	return getandsave

if __name__ == '__main__':
	cron = scheduler()
	model_list = [get_registered_scraper(r.scraper_class) for r in ModelRegistry.objects.all()]
	for scraper in model_list:
		scraperinst = scraper()
		cron.register(dolog(scraperinst), 20)
	cron.main()