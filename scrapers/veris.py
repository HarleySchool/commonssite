import requests
from commonssite.settings import veris_host, veris_port, veris_uname, veris_password
from commonssite.scrapers.xml_import import etree

def get_xml_string(channel):
	full_url = "http://%s:%d/setup/devicexml.cgi?ADDRESS=%d&TYPE=DATA" % (veris_host, veris_port, channel)
	req = requests.get(full_url, auth=(veris_uname, veris_password))
	return str(req.text)

if __name__ == '__main__':
	xml_obj_1 = etree.fromstring(get_xml_string(3))
	xml_obj_2 = etree.fromstring(get_xml_string(4))
	print etree.tostring(xml_obj_1, pretty_print=True)
	# TODO parse fully into dict
	print xml_obj_1.find('./devices/device/name').text,
	print xml_obj_1.find('./devices/device/status').text,
	print xml_obj_1.find('./devices/device/records/record/time').text