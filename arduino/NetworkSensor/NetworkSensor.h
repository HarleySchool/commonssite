/* 
	NetworkSensor.h Library for creating a data logging sensor which serves its data over Ethernet
	Written by Richard Lange, March 2014
*/
#ifndef NETWORK_SENSOR_H
#define NETWORK_SENSOR_H

#include "Arduino.h"
#include <SPI.h>
#include <Ethernet.h>
#include <SD.h>
#include <EthernetUdp.h> // used to sync time with NTP
#include <Time.h>

// Default pins for Ethernet shield with an SD card slot
#define SDSS 4 // NOTE that pins 11, 12, and 13 are also reserved for SD communication. see here: http://arduino.cc/en/Reference/SDCardNotes
#define ETHSS 10
#define LOGFILE "DATA.LOG"
#define SERVERPORT 80

// definitions used for NTP time sync
#define UDP_PORT 8888
// default sync time set to every 6 hours (measured in minutes)
#define NTP_SYNC 360L
// NTP protocol specifies a header with 4x16 values. We use 3 of them (ignoring checksum), so 3x16=48
#define NTP_PACKET_SIZE 48
// NTP, as specified in the protocol, communicates on port 123
#define NTP_PORT 123

/*
 * BIG TODO: better file format on SD. overwriting every line is not an efficient use of space.
 */

// This class is inspired by the work found here: https://github.com/OpenReefs/Open-Reefs-Controllers/tree/master/examples/ntpSync
// which is covered by the Createive Commons license.
// License: http://creativecommons.org/licenses/by-nc-sa/3.0/)
class TimeNTP{
public:
	// public-facing functions for getting current time
	unsigned int year();
	unsigned int month();
	unsigned int day();
	unsigned int hour();
	unsigned int minute();
	unsigned int second();
	unsigned long now();

	TimeNTP();
	TimeNTP(unsigned long sync_period_minutes);

	// check if sync period is up (and if so, sync time)
	// optional to force update
	void checkSync(bool force_update=false, int max_retries=4);
private:
	// send packet to the server requesting an update
	void sendNTPpacket(IPAddress& address);
	// read response packet (to be used after sendNTPpacket)
	unsigned long readResponseAsEpoch();

	// keep track of sync time (very infrequent updates; more than once per day is pushing it)
	// last_update is initialized to 0L, which is useful as a check for whether it has been synced at all
	unsigned long last_update, sync_period;

	IPAddress ip;
	EthernetUDP Udp;
};

class NetworkSensor{
public:
	// dummy constructor for declarations
	NetworkSensor();
	// constructor (called when object is created; responsible for initializing variables)
	NetworkSensor(uint8_t mac[], uint8_t ip[]);
	// destructor (called when object is destroyed; responsible for cleaning up (i.e. deallocate memory))
	~NetworkSensor();

	// function to serve data
	void serve();

	// function to get UTC time over the network (using the TimeNTP)
	unsigned long getTime();

	// logging functions
	void logf(String name, float value, unsigned int precision);
	void logi(String name, int value);
	void logs(String name, String value);
private:
	// the initialized variable is a bit of a hack to get around the problem of needing a generic constructor.
	// surely there is a better way, but this works!
	bool initialized;
	
	// Reference to the server object
	EthernetServer server;

	// Network-based clock for keeping track of time accurately
	TimeNTP clock;

	// initialization helpers
	void initSD();
	void initEthernet(uint8_t mac[], uint8_t ip[]);

	// Write given name:value pair to the log
	void log(String name, String stringifiedValue);

	// Set Slave-Select pins enabling ethernet usage
	inline void ethernetMode()	{ digitalWrite(SDSS, HIGH); digitalWrite(ETHSS, LOW); }
	// Set Slave-Select pins enabling SD card usage
	inline void SDMode()		{ digitalWrite(ETHSS, HIGH); digitalWrite(SDSS, LOW); }

	// returns string of val with number of decimal places determine by precision
	// NOTE: precision is 1 followed by the number of zeros for the desired number of decimial places
	// example: floatToString( 3.1415, 100); // returns "3.14" (two decimal places)
	String floatToString(float val, unsigned int precision){
		String s = String(int(val)) + String(".");
	    unsigned int frac;
	    if(val >= 0)
	        frac = (val - int(val)) * precision;
	    else
	        frac = (int(val)- val ) * precision;
	    s += String(frac);
	    return s;
	}
};

#endif // NETWORK_SENSOR_H