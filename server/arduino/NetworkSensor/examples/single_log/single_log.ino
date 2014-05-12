#include <SPI.h>
#include <Ethernet.h>
#include <Time.h>
#include <NetworkSensor.h>

byte mac[] = { 0xDC, 0x50, 0xA1, 0x42, 0x83, 0x7E };
byte ip[] = {10, 1, 6, 106};

NetworkSensor sensor;
unsigned int last_log = 0;

void setup(){
  sensor.begin(mac, ip);
  sensor.logf("Pi", 3.14159); // log a floating point with 3 decimal places of precision
  sensor.logi("BigNumber", 12345); // log an integer
  sensor.logs("Message", "Hello world");
}

void loop(){
  // first thing in the loop: serve existing data
  sensor.input_output();
}
