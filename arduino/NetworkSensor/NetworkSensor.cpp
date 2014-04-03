#include "NetworkSensor.h"

NetworkSensor::NetworkSensor() : server(SERVERPORT), initialized(false) {}

NetworkSensor::NetworkSensor(uint8_t mac[], uint8_t ip[]) : server(SERVERPORT), initialized(true)
{
	// Serial connection for debugging
	Serial.begin(9600);
	
	// SS (Slave Select) pins are handled by SDMode() and ethernetMode()
	pinMode(ETHSS, OUTPUT);
	pinMode(SDSS,  OUTPUT);

	// initialize
	initSD();
	initEthernet();
}

NetworkSensor::~NetworkSensor(){}

void NetworkSensor::initSD()
{
	// SD pin configuration
	SDMode();
	// see if the card is present and can be initialized:
	if (SD.begin(SDCS)) {
		Serial.println("SD card initialized.");
		clearLogFile();
	} else{
		initialized = false;
		Serial.println("failed, or card not plugged in");
	}
}

void NetworkSensor::initEthernet(uint8_t mac[], uint8_t ip[])
{
	// Server initialization
	ethernetMode()
	IPAddress ip_addr(ip[0], ip[1], ip[2], ip[3]);
	Ethernet.begin(mac, ip_addr);
	Serial.print("Opened server connection on ");
	Serial.print(ip[0]); Serial.print("."); Serial.print(ip[1]); Serial.print("."); Serial.print(ip[2]); Serial.print("."); Serial.println(ip[3]);
	server.begin();
}

void NetworkSensor::serve()
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return;
	}
	ethernetMode();
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

					String content = getCurrentFile();
					client.println("{");
					{
						// the format of the file is lines of 'Name : value,', so
						// no further processing is needed to make it json-style
						client.println(content);
					}
					client.println("}");

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

long NetworkSensor::getUTC()
{

}

void NetworkSensor::logf(String name, float value, unsigned int precision)
{
	log(name, floatToString(value, precision));
}

void NetworkSensor::logi(String name, int value)
{
	log(name, String(value));
}

void NetworkSensor::logs(String name, String value){
	String quoted_value = "\"" + value + "\"";
	log(name, quoted_value);
}

void NetworkSensor::log(String name, String stringifiedValue)
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return;
	}
	SDMode();
	// create character array buffers (used when converting Strings to char[]s)
	char buf1[256];
	// get current contents of log file
	String contents = getCurrentFile();
	// surround 'name' with quotes
	String quoted_name = String("\"") + name + String("\"");

	// --------------------------------------------------------------------------- //
	// Now we search for a line with that name and replace it if it exists         //
	// (essentially a map from name->value that gets overwritten with new values)  //
	// --------------------------------------------------------------------------- //

	// lines start with the quoted name, so search for the existing line
	int line_end = -1, line_start = str_search(contents.toCharArray(), quoted_name.toCharArray(), 0);
	if(line_start > -1){
		// if we found a line with the given name, search for the end of the line
		// so we can splice it out from start to end
		line_end = str_search(contents.toCharArray(), "\n", line_start);
	}
	// Debugging
	{
		Serial.print("Replacement line: [");
		Serial.print(line_start); Serial.print(", "); Serial.print(line_end);
		Serial.println("]");
	}
	// clear existing content (to be overwritten anyway)
	clearLogFile();
	// open the file for writing
	File data_file = SD.open(LOGFILE, FILE_WRITE);
	if(data_file){
		// writing now happens in 3 parts:
		//	1) content up-to-line
		if(line_start > -1){
			memset(buf, 0, 128);
			String prev_content = contents.substring(0, line_start);
			prev_content.toCharArray(buf, 128);
			data_file.write(buf);
		}
		//	2) new-line
		memset(buf, 0, 128);
		String newline = quoted_name + " : " + stringifiedValue + ",\n";
		newline.toCharArray(buf, 128);
		data_file.write(buf);
		//	3) content after-line
		memset(buf, 0, 128);
		String post_content = contents.substring(line_end+1);
		post_content.toCharArray(buf, 128);
		data_file.write(buf);
		// for changes to take effect, file must be closed
		data_file.close();
	} else{
		Serial.println("Could no open file for splicing.");
	}
}

void NetworkSensor::clearLogFile()
{
	// remove log file if it exists
	if(SD.exists(LOGFILE)) SD.remove(LOGFILE);
	// create empty log file
	File data_file = SD.open(LOGFILE, FILE_WRITE);
	data_file.close();
}

String NetworkSensor::getCurrentFile()
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return String("");
	}
	String content("");
	File data_file = SD.open(LOGFILE);
	if(data_file){
		Serial.println("===============");
		char c;
		while(data_file.available() && (c=data_file.read()) != EOF){
			Serial.print(c);
			content += c;
		}
		data_file.close();
		Serial.println("===============");
	} else{
		Serial.println("getCurrentFile unable to open file.");
	}
	return content;
}