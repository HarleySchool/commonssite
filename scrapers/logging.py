import time
import threading
import heapq
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
			nextgo = t + interval
			heapq.heappush(self.heap, (nextgo, func))
	def main(self):
		self.startheap()
		while True:
			## Insert thing to do here ##
			# should not take over the time speced in interval
			# don't even cut it close
			# use run_theaded to clear the main thread
			#############################
			func, nexttime = self.popandnext()
			self.run_threaded(func)
			sleeptime = nexttime - time.time()
			if sleeptime < 1 and sleeptime > -3:
				pass
			elif sleeptime < -3:
				print 'Sleep time error, heave you suspended your computer recently?'
				exit()
			else:
				time.sleep(sleeptime)

if __name__ == '__main__':
	def hi():
		print 'hi from hi'
	def lo():
		print 'hi from lo'
	timing = scheduler()
	timing.register(hi, 2)
	timing.register(lo, 4)
	timing.main()