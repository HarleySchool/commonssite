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

#define LOGFILE  "DATA.LOG"
// Default pins for Ethernet shield with an SD card slot
const int SDSS = 4; // NOTE that pins 11, 12, and 13 are also reserved for SD communication. see here: http://arduino.cc/en/Reference/SDCardNotes
const int ETHSS = 10;
const int SERVERPORT = 80;
const int NTP_SYNC_MINUTES = 12*60; // sync every 12 hours

/*
 * BIG TODO: better file format on SD. overwriting every line is not an efficient use of space.
 */

/////////////////////////
// NetworkSensor Class //
/////////////////////////

class NetworkSensor{
public:
  // dummy constructor for declarations
  NetworkSensor();
  // destructor (called when object is destroyed; responsible for cleaning up (i.e. deallocate memory))
  ~NetworkSensor();

  // responsible for initializing variables
  void begin(uint8_t mac[], uint8_t ip[]);

  // function to serve data
  void serve();

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

  // initialization helpers
  void initSD();
  void initEthernet(uint8_t mac[], uint8_t ip[]);

  // Write given name:value pair to the log
  void log(String name, String stringifiedValue);

  // Set Slave-Select pins enabling ethernet usage
  inline void ethernetMode()  { digitalWrite(SDSS, HIGH); digitalWrite(ETHSS, LOW); }
  // Set Slave-Select pins enabling SD card usage
  inline void SDMode()    { digitalWrite(ETHSS, HIGH); digitalWrite(SDSS, LOW); }

  // Time is synchronized with an NTP server
  void syncTimeNTP();
  inline bool isTimeSynced() { return last_time_sync != 0UL; }
  unsigned long last_time_sync, time_sync_interval;

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