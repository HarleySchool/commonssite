/* 
	NetworkSensor.h Library for creating a data logging sensor which serves its data over Ethernet
	Written by Richard Lange, March 2014
*/
#ifndef NETWORK_SENSOR_H
#define NETWORK_SENSOR_H

#include "Arduino.h"
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h> // used to sync time with NTP
#include <SD.h>
#include <map>

// Default pins for Ethernet shield with an SD card slot
#define SDSS 4 // NOTE that pins 11, 12, and 13 are also reserved for SD communication. see here: http://arduino.cc/en/Reference/SDCardNotes
#define ETHSS 10
#define LOGFILE "DATA.LOG"
#define SERVERPORT 80

/*
 * BIG TODO: better file format on SD. overwriting every line is not an efficient use of space.
 */

class NetworkSensor{
public:
	// dummy constructor for declarations
	NetworkSensor();
	// constructor (called when object is created; responsible for initializing variables)
	NetworkSensor(uint8_t mac[], uint8_t ip[]);
	// destructor (called when object is destroyed; responsible for cleaning up (i.e. deallocate memory))
	~NetworkSensor();

	// logging functions
	void logf(String name, float value, unsigned int precision);
	void logi(String name, int value);
	void logs(String name, String value);

	// function to serve data
	void serve();

	// function to get UTC time over the network
	// For reference: http://arduino.cc/en/Tutorial/UdpNTPClient
	long getUTC();
private:
	// the initialized variable is a bit of a hack to get around the problem of needing a generic constructor.
	// surely there is a better way, but this works!
	bool initialized;
	
	// Reference to the server object
	EthernetServer server;

	// keeping time with global clock. 
	// logged UTC time is `millis() + UTCoffset`
	long UTCoffset;

	// Get current log file contents
	String getCurrentFile();

	// Write given name:value pair to the log
	void log(String name, String stringifiedValue);

	// Set Slave-Select pins enabling ethernet usage
	inline void ethernetMode()	{ digitalWrite(SDSS, HIGH); digitalWrite(ETHSS, LOW); }
	// Set Slave-Select pins enabling SD card usage
	inline void SDMode()		{ digitalWrite(ETHSS, HIGH); digitalWrite(SDSS, LOW); }

	// initialization helpers
	void initSD();
	void initEthernet(uint8_t mac[], uint8_t ip[]);

	// deletes and recreates the log file
	// TODO - multiple log files handled more intelligently
	void clearLogFile();

	/////////////////////////////////
	// String manipulation helpers //
	/////////////////////////////////

	// Locate a substring within another string.
	// much like the built-in strstr function, but with an optional start offset 
	int str_search(const char[] s, const char[] sub, int start=0){
		// &s[start] works like this:
		// char c = s[start];   // c is the character at index 'start'
		// char* subarray = &c; // arrays are just pointers, so the address of c is like an array starting at 'start'
		return strstr(&s[start], sub);
	}

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