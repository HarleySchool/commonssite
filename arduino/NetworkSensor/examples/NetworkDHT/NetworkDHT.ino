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
#define N_SENSORS 2

DHT *psensors[N_SENSORS];

byte mac[] = { 0xDC, 0x50, 0xA1, 0x42, 0x83, 0x7E };
byte ip[] = {10, 1, 6, 106};
NetworkSensor sensor;

int cur_dht;

void setup(){
  // debugging
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  sensor.begin(mac, ip);
  // initialize selection pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  // initialize serial commands interface
  Serial.begin(9600);
  Serial.println("Setup Complete");
  cur_dht = 0;
  // initialize DHT objects
  for(int i=0; i<N_SENSORS; i++){
    psensors[i] = new DHT(DHTPIN, DHT22);
    psensors[i]->begin();
  }
  muxSelect(7); // select a non-sensor
  delay(2000); // delay 1 second to let sensors stabilize
}

void muxSelect(int which){
  if(0 <= which && which < 8){
    digitalWrite(S0, which & 0x01);
    digitalWrite(S1, which & 0x02);
    digitalWrite(S2, which & 0x04);
    Serial.print("Selected mux ");
    Serial.println(which);
  } else{
     Serial.print("Invalid mux select: ");
     Serial.println(which);
  } 
}

void loop(){
  sensor.input_output();
  muxSelect(cur_dht);
  delay(100);
  // read and print DHT sensor values
  float h = psensors[cur_dht]->readHumidity();
  float t = psensors[cur_dht]->readTemperature();
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (isnan(t) || isnan(h) || (h == 0 && t == 0)) {
    Serial.println("Failed to read from DHT");
    digitalWrite(3-cur_dht, HIGH);
    delay(200);
  } else {
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
    digitalWrite(3-cur_dht, LOW);
  }
  cur_dht = (cur_dht + 1) % N_SENSORS;
}

