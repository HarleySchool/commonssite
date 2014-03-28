#include "NetworkSensor.h"

NetworkSensor::NetworkSensor() : server(SERVERPORT), initialized(false) {}

NetworkSensor::NetworkSensor(uint8_t mac[], uint8_t ip[]) : server(SERVERPORT), initialized(true)
{
	// Serial connection for debugging
	Serial.begin(9600);
	// SD pin configuration
	pinMode(ETHCS, OUTPUT);
	Serial.print("Initializing SD card...");
	// see if the card is present and can be initialized:
	if (SD.begin(SDCS)) {
		Serial.println("SD card initialized.");
		// create empty log file
		File data_file = SD.open(LOGFILE, FILE_WRITE);
		if(data_file){
			data_file.write("");
			data_file.close();
		} else{
			Serial.println("Could not create log file.");
		}
	} else{
		initialized = false;
		Serial.println("SD initialization failed, or card not plugged in");
	}
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

					String content = get_current_file();
					client.println("{");
					{
						// the format of the file is lines of 'Name : value,', so
						// no further processing is needed to make it json-style
						client.println(content);
					}
					client.println("}");

					Serial.println("{");
					{
						Serial.println(content);
					}
					Serial.println("}");
					
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
	char buf[128];
	String contents = get_current_file();
	String quoted_name = "\""+name+"\"";
	int line_end = -1;
	int line_start = str_search(contents, quoted_name, 0); // lines start with 'quoted_name', so search for the existing line
	if(line_start > -1){
		// find the index of the end of the line so we can splice it out from start to end
		line_end = str_search(contents, "\n", line_start);
	}
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
		if(line_end > -1){
			String post_content = contents.substring(line_end+1);
			post_content.toCharArray(buf, 128);
			data_file.write(buf);
		}
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
	String contents = "";
	if(data_file){
		// read from the file until there's nothing else in it:
		while (data_file.available()) {
			contents += char(data_file.read());
		}
		// close the file:
		data_file.close();
	} else{
		Serial.println("get_current_file unable to open file.");
	}
	return contents;
}