/* NetworkDHT.ino
   written by Richard Lange. April 2014.

   DHT sensors (e.g. DHT11, DHT22) are combination temperature and humidity sensors.
   In this circuit, we connect to up to 8 DHT sensors using only 4 data lines and 2
   power lines. This is possible using a CD74HC4051E multiplexer/demultiplexer
   from texas instruments.
   In theory, this pattern could be extended for as many sensors as are needed.
   
   Power lines = 2 wires
   Data bus    = 1 bit
   Mux select  = 3 bits (2^3 = 8 sensors)

   Data is logged and served over ethernet using the NetworkSensor library. Note that the
   Ethernet Shield (on an Uno) uses pin 10, so we need to be careful not to wire sensors
   there.
*/

#include <DHT.h>
#include <Time.h>
#include <SPI.h>
#include <Ethernet.h>
#include <NetworkSensor.h>

// MUX selection bits
#define S0 7
#define S1 8
#define S2 9

// Data pin
#define DHTPIN 6
// Can specify up to 8. The current logging code is only set up to handle 2, however.
#define N_SENSORS 2

// A DHT object for each sensor
DHT *psensors[N_SENSORS];

// Random MAC address
byte mac[] = { 0xDC, 0x50, 0xA1, 0x42, 0x83, 0x7E };
// IP address looked up using the Ethernet>DhcpAddressPrinter example sketch.
// ***********************************************
// * CHANGE IP TO WHATEVER YOUR LOCAL ADDRESS IS *
// ***********************************************
byte ip[] = {10, 1, 6, 106};
// the NetworkSensor instance
char* float_names[] = {"H0", "T0", "H1", "T1"};
NetworkSensor sensor(NULL,0,float_names,4,NULL,0);

// In order to call sensor.input_output() as frequently as possible,
// we only poll a single DHT sensor per loop() iteration. (This is OK
// because NetworkSensor keeps the timestamps for us!)
// cur_dht is one of {0, 1, ..., N_SENSORS-1}. It is the sensor which
// is active in the current loop() iteration, and is incremented at 
// the end of each loop()
int cur_dht;

void setup(){
  // debugging
  pinMode(2, OUTPUT); // an LED attached to pin 2 will light up any time there is a read error from sensor #1
  pinMode(3, OUTPUT); // ..likewise, but pin 3 lights up for sensor #0
  // initialize the NetworkSensor instance
  sensor.begin(mac, ip);
  // initialize selection pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  // initialize serial printing interface for debugging
  Serial.begin(9600);
  Serial.println("Setup Complete");
  // initialize current sensor to #0
  cur_dht = 0;
  // initialize each of the DHT objects
  for(int i=0; i<N_SENSORS; i++){
    psensors[i] = new DHT(DHTPIN, DHT22);
    psensors[i]->begin();
  }
  muxSelect(7); // select a non-sensor to let them clear
  delay(1500); // delay 1.5 seconds to let sensors stabilize (the datasheet recommends 1 second, but 1.5 gets us a higher success rate)
}

// This function takes a selection ({0 .. 7}) and activates
// that branch of the Mux
void muxSelect(int which){
  // ensure that we're within range
  if(0 <= which && which < 8){
    // & is 'bitwise AND', which in this case
    // is acting as a "mask"
    // 0x01 is 00000001
    // 0x02 is 00000010
    // 0x04 is 00000100
    // 0x08 is 00001000
    // etc..
    digitalWrite(S0, which & 0x01);
    digitalWrite(S1, which & 0x02);
    digitalWrite(S2, which & 0x04);
    Serial.print("Selected mux ");
    Serial.println(which);
  } else{
     Serial.print("Invalid mux selection: ");
     Serial.println(which);
  }
  delay(50);
}

void loop(){
  // input_output provides our logged data over the internet
  sensor.input_output();

  // now we start reading and logging the current sensor 
  muxSelect(cur_dht);
  // read and print DHT sensor values (the DHT library takes care of communicating with the sensor here)
  float h = psensors[cur_dht]->readHumidity();
  float t = psensors[cur_dht]->readTemperature();
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  // Note that although the DHT library's example only checks isnan, we occasionally get
  // incorrect "valid" responses when they are all zeros. ("valid" because the checksum works: (0+0+0+0 & 0xFF == 0))
  if (isnan(t) || isnan(h) || (h == 0 && t == 0)) {
    Serial.println("Failed to read from DHT");
    digitalWrite(3-cur_dht, HIGH); // turn on status LED indicating that this sensor had an error
    delay(500); // give the sensors a moment to catch up
  } else {
    // If reading is valid, log it!
    // Note that we could choose any name we want. T0/H0/T1/H1 are short and sweet and work fine for this example.
    // Other available functions are logs for strings and logi for integers
    t = psensors[cur_dht]->convertCtoF(t);
    switch(cur_dht){
    case 0:
      sensor.logf("T0", t);
      sensor.logf("H0", h);
      break;
    case 1:
      sensor.logf("T1", t);
      sensor.logf("H1", h);
      break;
    };
    digitalWrite(3-cur_dht, LOW); // turn off status LED indicating no error.
  }
  cur_dht = (cur_dht + 1) % N_SENSORS; // increment the "current" sensor, wrapping around to 0 when we reached the end
}
