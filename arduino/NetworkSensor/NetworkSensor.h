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

// Default pins for Ethernet shield with an SD card slot
#define SDCS 4 // NOTE that pins 11, 12, and 13 are also reserved for SD communication. see here: http://arduino.cc/en/Reference/SDCardNotes
#define ETHCS 10
#define LOGFILE "data.log"
#define SERVERPORT 80

class NetworkSensor{
public:
	NetworkSensor(); // dummy constructor for declarations
	NetworkSensor(uint8_t mac[], uint8_t ip[]); // constructor (called when object is created; responsible for initializing variables)
	~NetworkSensor(); // destructor (called when object is destroyed; responsible for cleaning up (i.e. deallocate memory))
	// logging functions
	void logf(String name, float value, unsigned int precision);
	void logi(String name, int value);
	void logs(String name, String value);
	// function to serve data
	void serve();
private:
	// ETHERNET CONFIGURATION
	EthernetServer server;
	bool initialized;
	// SD writing helper
	String get_current_file();
	void log(String name, String stringifiedValue);


	/////////////////////////////////
	// String manipulation helpers //
	/////////////////////////////////

	int str_search(String s, String sub, int start){
		for(unsigned int i=start; i<s.length()-sub.length()+1; i++){
			bool found = true;
			for(unsigned int j=0; j<sub.length(); j++){
				if(s.charAt(i+j) != sub.charAt(j)){
					found = false;
					break;
				}
			}
			if(found) return i;
		}
		return -1;
	}

	String floatToString( float val, unsigned int precision){
		// returns string of val with number of decimal places determine by precision
		// NOTE: precision is 1 followed by the number of zeros for the desired number of decimial places
		// example: floatToString( 3.1415, 100); // returns "3.14" (two decimal places)
		String s = int(val) + ".";
	    unsigned int frac;
	    if(val >= 0)
	        frac = (val - int(val)) * precision;
	    else
	        frac = (int(val)- val ) * precision;
	    s += frac;
	    return s;
	}
};

#endif // NETWORK_SENSOR_H