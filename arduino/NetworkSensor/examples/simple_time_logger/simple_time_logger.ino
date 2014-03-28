#include <SPI.h>
#include <Ethernet.h>
#include <SD.h>
#include <NetworkSensor.h>

byte mac[] = { 0xDC, 0x50, 0xA1, 0x42, 0x83, 0x7E };
byte ip[] = {10, 1, 6, 106};

NetworkSensor sensor;
unsigned int last_log = 0;

void setup(){
  sensor = NetworkSensor(mac, ip);
}

void loop(){
  // first thing in the loop: serve existing data
  sensor.serve();
  // log new data
  if(millis() - last_log > 1000){
    last_log = millis();
    //sensor.logi("Time", last_log); // log an integer
    //sensor.logs("A String", "a string value"); // log a string
    //sensor.logf("Pi", 3.14159, 1000); // log a floating point with 3 decimal places of precision
  }
}
