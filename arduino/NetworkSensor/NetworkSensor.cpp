#include "NetworkSensor.h"

NetworkSensor::NetworkSensor() : server(SERVERPORT), initialized(false) {}

NetworkSensor::NetworkSensor(uint8_t mac[], uint8_t ip[]) : server(SERVERPORT), initialized(true)
{
	// Serial connection for debugging
	Serial.begin(9600);
	// SD pin configuration
	pinMode(ETHCS, OUTPUT);
	Serial.print("Initializing SD card... ");
	// see if the card is present and can be initialized:
	if (SD.begin(SDCS)) {
		Serial.println("SD card initialized.");
		// remove log file if it exists
		if(SD.exists(LOGFILE)) SD.remove(LOGFILE);
		// create empty log file
		File data_file = SD.open(LOGFILE, FILE_WRITE);
		data_file.close();
		// print content (Debug)
		data_file = SD.open(LOGFILE);
		if(data_file){
			Serial.println("===============");
			while(data_file.available()) Serial.print(data_file.read());
			data_file.close();
			Serial.println("===============");
		}
	} else{
		initialized = false;
		Serial.println("failed, or card not plugged in");
	}
	// Server initialization
	// IPAddress ip_addr(ip[0], ip[1], ip[2], ip[3]);
	// Ethernet.begin(mac, ip_addr);
	// Serial.print("Opened server connection on ");
	// Serial.print(ip[0]); Serial.print("."); Serial.print(ip[1]); Serial.print("."); Serial.print(ip[2]); Serial.print("."); Serial.println(ip[3]);
	// server.begin();
	Serial.println("skipped ethernet setup");
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
		delay(1);
		client.stop();
	}
}

void NetworkSensor::logf(String name, float value, unsigned int precision)
{
	log(name, floatToString(value, precision));
}

void NetworkSensor::logi(String name, int value)
{
	log(name, String(value));
}

void NetworkSensor::log(String name, String stringifiedValue)
{
	Serial.print("beginning log of ");
	Serial.println(stringifiedValue);
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return;
	}
	char buf[128];
	String contents = get_current_file();
	String quoted_name = String("\"") + name + String("\"");
	int line_end = -1;
	int line_start = str_search(contents, quoted_name, 0); // lines start with 'quoted_name', so search for the existing line
	if(line_start > -1){
		// find the index of the end of the line so we can splice it out from start to end
		line_end = str_search(contents, "\n", line_start);
	}
	Serial.print("Replacement line: [");
	Serial.print(line_start); Serial.print(", "); Serial.print(line_end);
	Serial.println("]");
	File data_file = SD.open(LOGFILE, FILE_WRITE);
	if(data_file){
		// writing now happens in 3 parts:
		//	1) content up-to-line
		if(line_start > -1){
			String prev_content = contents.substring(0, line_start);
			prev_content.toCharArray(buf, 128);
			data_file.write(buf);
		}
		//	2) new-line
		String newline = quoted_name + " : " + stringifiedValue + ",\n";
		newline.toCharArray(buf, 128);
		data_file.write(buf);
		//	3) content after-line
		String post_content = contents.substring(line_end+1);
		post_content.toCharArray(buf, 128);
		data_file.write(buf);
		// for changes to take effect, file must be closed
		data_file.close();
	} else{
		Serial.println("Could no open file for splicing.");
	}
}

String NetworkSensor::get_current_file()
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return "";
	}
	File data_file = SD.open(LOGFILE);
	if(data_file){
		Serial.println("===============");
		while(data_file.available()) Serial.print((char)data_file.read());
		data_file.close();
		Serial.println("===============");
	} else{
		Serial.println("get_current_file unable to open file.");
	}
	return "";
}