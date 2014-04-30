/* 
  NetworkSensor.h Library for creating a data logging sensor which serves its data over Ethernet
  Written by Richard Lange, April 2014

  We are not using the SD library because of its large memory footprint and because we serve only the most recent data
  (the data is permanently stored elsewhere)
*/
#ifndef NETWORK_SENSOR_H
#define NETWORK_SENSOR_H

#include "Arduino.h"
#include <SPI.h>
#include <Ethernet.h>
#include <Time.h>

// Default pins for Ethernet shield
const int ETHSS = 10;
const int SDSS = 4;
const int SERVERPORT = 80;
const int BUFFER_SIZE = 8; // size of initial TupleArrays (no realloc for up to 8 floats/ints/strings)

template <typename T>
struct TimestampValueArray{
  time_t* times; // array of epoch times
  char** names;  // parallel array of names
  T* values;     // parallel array of values (times[i], names[i], and values[i] are a single point)
  time_t offset_millis;
  int size, capacity; // dynamically growing array stuff

  TimestampValueArray(): offset_millis(0), size(0), capacity(BUFFER_SIZE)
  {
    times = (time_t*) malloc(sizeof(time_t) * capacity);
    names = (char**) malloc(sizeof(char*) * capacity);
    values = (T*) malloc(sizeof(T) * capacity);
  }

  ~TimestampValueArray()
  {
    free(times);
    for(int i=0; i<size; i++) free(names[i]);
    free(names);
    free(values);
  }

  void set(String name, T value)
  {
    char buf[32];
    name.toCharArray(buf, 32);
    // search for existing name
    for(int i=0; i<size; ++i){
      if(strcmp(buf, names[i]) == 0){
        // update existing value and be done
        times[i] = millis() + offset_millis;
        values[i] = value;
        return;
      }
    }
    // if we made it this far, then 'name' wasn't found and we need to create a new pair.
    // Before jumping into that, we should check if the arrays need to be expanded
    if(size == capacity){
      // double the capacity (it's more efficient this way than simply adding an additional slot)
      capacity *= 2;
      times = (time_t*) realloc(times, sizeof(time_t) * capacity);
      names = (char**) realloc(names, sizeof(char*) * capacity);
      values = (T*) realloc(values, sizeof(T) * capacity);
    }
    // add the new value
    times[size] = millis() + offset_millis;
    // create character array and copy name to it
    int null_terminated_length = name.length()+1;
    names[size] = (char*) malloc(sizeof(char) * null_terminated_length);
    name.toCharArray(names[size], null_terminated_length);
    // copy value
    values[size] = value;
    size++;
  }
};

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

  // the do-all function that is called every loop(). it handles serving data over ethernet.
  void input_output();

  // logging functions
  void logf(String name, float value);
  void logi(String name, int value);
  void logs(String name, String value);
private:
  // the initialized variable is a bit of a hack to get around the problem of needing begin() to be called.
  // surely there is a better way, but this works!
  bool initialized;
  
  // Reference to the server object
  EthernetServer server;

  // Arrays of each of the data types
  TimestampValueArray<float>  f_values;
  TimestampValueArray<int>    i_values;
  TimestampValueArray<String> s_values;

  // initialization helper
  void initEthernet(uint8_t mac[], uint8_t ip[]);

  // update time offset
  void remoteSetTime(time_t epoch);

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