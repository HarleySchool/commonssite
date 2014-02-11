import httplib, json, urllib, time
from settings import sma_host, sma_port
from pprint import pprint

devices = {
	'weather' : {
		'DevKey' : r'SENS0700:26877',
		'DevClass' : r'Sunny%20Sensor%20Box'
	},
	'power' : {
		'DevKey' : r'WRHV5K84:19120146',
		'DevClass' : r'Sunny%20Boy'
	}
}

status_pages = {
	'summary' : {
		'referer' : 'plant_devices_devfrm_single.htm',
		'updater' : 'dev_frm_single.ajax'
	},
	'details' : {
		'referer' : 'plant_current.htm',
		'updater' : 'current_values.ajax',
	},
}

def login(pw, connection=None):
	body = 'Password=%s' % pw
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': 'http://%s/home.htm' % sma_host,
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Content-Length': str(len(body))
	}
	if not connection:
		connection = httplib.HTTPConnection(sma_host, sma_port)
	req = connection.request("POST", '/login', body, headers)
	return connection.getresponse().read()

"""
REQUEST 1
GET /current_values.ajax HTTP/1.1
Host: 10.1.6.201
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
X-Prototype-Version: 1.4.0
Referer: http://10.1.6.201/plant_current.htm?DevKey=WRHV5K84:191201464&DevClass=Sunny%20Boy
Connection: keep-alive

REQUEST 2
GET /current_values.ajax HTTP/1.1
Host: 10.1.6.201
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
X-Prototype-Version: 1.4.0
Referer: http://10.1.6.201/plant_current.htm?DevKey=WRHV5K84:191201464&DevClass=Sunny%20Boy
Connection: keep-alive

MY REQUEST

"""

""
def get_data(dev_name, status_type, connection=None, attempts=3, retry_sleep=1.0):
	if not connection:
		connection = httplib.HTTPConnection(sma_host, sma_port)
	device_params = '&'.join(['%s=%s' % (key, value) for (key,value) in devices[dev_name].iteritems()])
	# Step 1 - connect to htm page
	htm_page_url = '/%s?%s' % (status_pages[status_type]['referer'], device_params)
	req1 = connection.request('GET', htm_page_url)
	connection.getresponse().read()
	# Step 2 - get JSON update
	ajax_page_url = "/%s" % status_pages[status_type]['updater']
	headers = {
		'Accept-Encoding' : 'gzip, deflate',
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language' : 'en-US,en;q=0.5',
		'Connection' : 'keep-alive',
		'Referer' : 'http://%s%s' % (sma_host, htm_page_url)
		}
	n_tries = 0
	tstart = time.time()
	while n_tries < attempts:
		n_tries += 1
		req2 = connection.request("GET", ajax_page_url, None, headers)
		resp_string = connection.getresponse().read()
		try:
			resp_json = json.loads(resp_string)
			if dev_name == "power" and status_type == "details" and not resp_json.get("CurrentValues", []):
				raise Exception("CurrentValues was empty")
			telapsed = time.time() - tstart
			print "SUCCESS AFTER %d TRIES AND %f SECONDS" % (n_tries, telapsed)
			return resp_string
		except Exception as e:
			print "Could not parse attempt #%d\n\t%s" % (n_tries, resp_string)
			print "THE ERROR WAS", e
		time.sleep(retry_sleep)
	print "get_data didn't work after %d tries" % attempts
	return None

def logout(connection=None):
	if not connection:
		connection = httplib.HTTPConnection(sma_host, sma_port)
	req = connection.request("GET", "/home_frameset.htm?Logout=true")
	return connection.getresponse().read()

def scrape():
	conn = httplib.HTTPConnection(sma_host, sma_port)
	from itertools import product as prod
	login("sma", conn)
	for dev, typ in prod(("weather", "power"), ("summary", "details")):
		print "\ngetting %s data for %s" % (typ, dev)
		print get_data(dev, typ, conn)
	logout(conn)
	conn.close()

if __name__ == '__main__':
	scrape()