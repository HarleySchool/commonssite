#include "NetworkSensor.h"

NetworkSensor::NetworkSensor() : initialized(false), server(SERVERPORT) {}

NetworkSensor::NetworkSensor(uint8_t mac[], uint8_t ip[]) : initialized(true), server(SERVERPORT)
{
	// Serial connection for debugging
	Serial.begin(9600);
	Serial.println("Serial connection ready.");
	
	// SS (Slave Select) pins are handled by SDMode() and ethernetMode()
	pinMode(ETHSS, OUTPUT);
	pinMode(SDSS,  OUTPUT);

	// initialize
	Serial.println("connecting SD");
	initSD();
	Serial.println("connecting Ethernet");
	initEthernet(mac, ip);

	// set up clock (important that it is after initEthernet())
	this->clock = TimeNTP(NTP_SYNC);
}

NetworkSensor::~NetworkSensor(){}

void NetworkSensor::serve()
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return;
	}
	ethernetMode();
	// make sure clock is synchronized
	this->clock.checkSync();
	// check for client connections and write requested data back
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

					String content("NO CONTENT YET, SORRY");
					client.println("{");
					{
						// the format of the file is lines of 'Name : value,', so
						// no further processing is needed to make it json-style
						client.println(content);
					}
					client.println("}");

					// for debugging
					Serial.println(content);
					
					break;
				}
				currentLineIsBlank = (c == '\n' || c == '\r');
			}
		}
		delay(1);
		client.stop();
	}
}

unsigned long NetworkSensor::getTime()
{
	return this->clock.now();
}

void NetworkSensor::logf(String name, float value, unsigned int precision)
{
	log(name, floatToString(value, precision));
}

void NetworkSensor::logi(String name, int value)
{
	log(name, String(value));
}

void NetworkSensor::logs(String name, String value)
{
	String quoted_value = "\"" + value + "\"";
	log(name, quoted_value);
}

void NetworkSensor::initSD()
{
	// SD pin configuration
	SDMode();
	// see if the card is present and can be initialized:
	if (SD.begin(SDSS)) {
		Serial.println("SD card initialized.");
	} else{
		initialized = false;
		Serial.println("failed, or card not plugged in");
	}
}

void NetworkSensor::initEthernet(uint8_t mac[], uint8_t ip[])
{
	// Server initialization
	ethernetMode();
	IPAddress ip_addr(ip[0], ip[1], ip[2], ip[3]);
	Ethernet.begin(mac, ip_addr);
	Serial.print("Opened server connection on ");
	Serial.print(ip[0]); Serial.print("."); Serial.print(ip[1]); Serial.print("."); Serial.print(ip[2]); Serial.print("."); Serial.println(ip[3]);
	server.begin();
}

void NetworkSensor::log(String name, String stringifiedValue)
{
	if(!initialized){
		Serial.println("ERROR: attempting to used uninitialized NetworkSensor (did you forget 'sensor=NetworkSensor(mac, ip)' ??");
		return;
	}
	SDMode();
	// TODO
}

// ---------------
// -- NTP Clock --
// ---------------


TimeNTP::TimeNTP() : last_update(0L), sync_period(0L)
{}

TimeNTP::TimeNTP(unsigned long sync_period_minutes)
: last_update(0L), sync_period(sync_period_minutes * 60000L)
{
	// based on a query from pool.ntp.org
	// NOTE that this may become obsolete. The correct way to do it
	// would be to do our own DNS on pool.ntp.org, but that is too
	// complicated for now.
	ip = IPAddress(166, 70, 136, 41);
	Udp.begin(UDP_PORT);
}

void TimeNTP::checkSync(bool force_update, int max_retries)
{
	// check if update needed
	if(force_update || (millis() - last_update) > sync_period){
		unsigned long epochTime = 0L;
		int tries = 0;
		while(epochTime == 0L && tries++ < max_retries){
			Serial.println("syncing NTP");
			sendNTPpacket(this->ip);
			delay(1000);
			epochTime = readResponseAsEpoch();
		}
		// update if successful
		if(epochTime != 0L){
			last_update = millis();
			setTime(epochTime);
			Serial.print("Time synced! it is now ");
			Serial.print(this->month());
			Serial.print("/");
			Serial.print(this->day());
			Serial.print("/");
			Serial.print(this->year());
			Serial.print(" ");
			Serial.print(this->hour());
			Serial.print(":");
			Serial.print(this->minute());
			Serial.print(":");
			Serial.println(this->second());
		} else{
			Serial.println("Sync failed");
		}
	}
}

unsigned long TimeNTP::now()
{
	if(last_update > 0L) return now();
	else return 0L;
}

unsigned int TimeNTP::year()
{
	if(last_update > 0L) return year();
	else return 0L;
}

unsigned int TimeNTP::month()
{
	if(last_update > 0L) return month();
	else return 0L;
}

unsigned int TimeNTP::day(){
	if(last_update > 0L) return day();
	else return 0L;
}

unsigned int TimeNTP::hour(){
	if(last_update > 0L) return hour();
	else return 0L;
}

unsigned int TimeNTP::minute(){
	if(last_update > 0L) return minute();
	else return 0L;
}

unsigned int TimeNTP::second(){
	if(last_update > 0L) return second();
	else return 0L;
}

void TimeNTP::sendNTPpacket(IPAddress& address)
{
	// consume and discard all existing requests
	while(Udp.parsePacket() > 0);
	// PROTOCOL SPECIFICATION: http://tools.ietf.org/html/rfc958#appendix-A
	// (or see the Time>TimeNTP example that comes with Arduino)
	// create byte buffer
	byte packetBuffer[NTP_PACKET_SIZE];
	// clear buffer to zeros
	memset(packetBuffer, 0, NTP_PACKET_SIZE);
	// set packet data as an NTP request
	packetBuffer[0]  = 0b11100011;
	packetBuffer[1]  = 0;
	packetBuffer[2]  = 0xEC;
	packetBuffer[3]  = 6;
	packetBuffer[12] = 49;
	packetBuffer[13] = 0x4E;
	packetBuffer[14] = 49;
	packetBuffer[15] = 52;
	Udp.beginPacket(address, NTP_PORT);
	Udp.write(packetBuffer, NTP_PACKET_SIZE);
	Udp.endPacket();
}

unsigned long TimeNTP::readResponseAsEpoch()
{
	// PROTOCOL SPECIFICATION: http://tools.ietf.org/html/rfc958#appendix-B
	if(Udp.parsePacket() >= NTP_PACKET_SIZE){
		byte packetBuffer[NTP_PACKET_SIZE];
		Udp.read(packetBuffer, NTP_PACKET_SIZE);
		unsigned long highWord, lowWord, epoch;
		highWord = word(packetBuffer[40], packetBuffer[41]);
		lowWord = word(packetBuffer[42], packetBuffer[43]);
		epoch = highWord << 16 | lowWord;
		// NTP specifies the # of seconds since 1900.
		// Unix time is since 1970.
		// There are 2208988800 seconds between 1900 and 1970  
		epoch -= 2208988800UL;
		return epoch;
	}
	return 0L;
}