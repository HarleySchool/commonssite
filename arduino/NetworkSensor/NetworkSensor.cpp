#include "NetworkSensor.h"

NetworkSensor::NetworkSensor() : server(SERVERPORT), initialized(false) {}

NetworkSensor::NetworkSensor(uint8_t mac[], uint8_t ip[]) : server(SERVERPORT), initialized(true)
{
	// Serial connection for debugging
	Serial.begin(9600);
	// Server initialization
	IPAddress ip_addr(ip[0], ip[1], ip[2], ip[3]);
	Ethernet.begin(mac, ip_addr);
	Serial.print("Opened server connection on ");
	Serial.print(ip[0]); Serial.print("."); Serial.print(ip[1]); Serial.print("."); Serial.print(ip[2]); Serial.print("."); Serial.println(ip[3]);
	server.begin();
}

NetworkSensor::~NetworkSensor(){}

void NetworkSensor::serve()
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return;
	}
	EthernetClient client = server.available();
	if (client) {
		Serial.println("Client available");
		// an http request ends with a blank line
		boolean currentLineIsBlank = true;
		while (client.connected()) {
			if (client.available()) {
				char c = client.read();
				// if we've gotten to the end of the line (received a newline
				// character) and the line is blank, the http request has ended,
				// so we can send a reply
				if (c == '\n' && currentLineIsBlank) {
					// send a standard http response header
					client.println("HTTP/1.1 200 OK");
					client.println("Content-Type: application/json");
					client.println();

					String json = this->as_json();
					client.println(json);

					// for debugging
					Serial.println(json);
					
					break;
				}
				currentLineIsBlank = (c == '\n' || c == '\r');
			}
		}
	}
}

void NetworkSensor::logf(String name, float value, unsigned int precision)
{
	log(name, floatToString(value, precision));
}

void NetworkSensor::logi(String name, int value)
{
	log(name, value+"");
}

void NetworkSensor::logs(String name, String value)
{
	log(name, "\""+value+"\"");
}

void NetworkSensor::log(String name, String stringifiedValue)
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return;
	}
	recent_values.put(name, stringifiedValue);
}

String NetworkSensor::as_json(){
	String json = "{";
	for(auto itr=recent_values.begin(); itr!=recent_values.end(); ++itr){
		json += (*itr).first() + ":" + (*itr).second() + ",";
	}
	json += "}";
	return json;
}