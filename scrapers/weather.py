from weewx.drivers.vantage import Vantage

class ScraperWeather(object):

	def __init__(self):
		pass

	def get_data(self):
		v = Vantage(type='ethernet', host='10.1.6.203')
		return v.genDavisLoopPackets(1)

if __name__ == '__main__':
	from pprint import pprint
	scraper = ScraperWeather()
	[pprint(d) for d in scraper.get_data()]