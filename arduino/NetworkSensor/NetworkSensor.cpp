#include "NetworkSensor.h"

NetworkSensor::NetworkSensor()
: initialized(false), server(SERVERPORT), last_time_sync(0UL), time_sync_interval(NTP_SYNC_MINUTES*60000)
{}

NetworkSensor::~NetworkSensor(){}

void NetworkSensor::begin(uint8_t mac[], uint8_t ip[])
{
  // Serial connection for debugging
  Serial.begin(9600);
  
  // SS (Slave Select) pins are handled by SDMode() and ethernetMode()
  pinMode(ETHSS, OUTPUT);
  pinMode(SDSS,  OUTPUT);

  initSD();
  initEthernet(mac, ip);

  // set up time synchronization
  syncTimeNTP();
}

void NetworkSensor::serve()
{
  if(!initialized){
    return;
  }
  ethernetMode();
  // check if it's time to re-sync the clock
  if((millis() - last_time_sync) > time_sync_interval){
    syncTimeNTP();
  }
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
          //Serial.println(content);
          
          break;
        }
        currentLineIsBlank = (c == '\n' || c == '\r');
      }
    }
    delay(1);
    client.stop();
  }
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
    //Serial.println("SD card initialized.");
  } else{
    initialized = false;
    //Serial.println("failed, or card not plugged in");
  }
}

void NetworkSensor::initEthernet(uint8_t mac[], uint8_t ip[])
{
  // Server initialization
  ethernetMode();
  IPAddress ip_addr(ip[0], ip[1], ip[2], ip[3]);
  Ethernet.begin(mac, ip_addr);
  ////Serial.print("Opened server connection on ");
  ////Serial.print(ip[0]); //Serial.print("."); //Serial.print(ip[1]); //Serial.print("."); //Serial.print(ip[2]); //Serial.print("."); //Serial.println(ip[3]);
  server.begin();
}

void NetworkSensor::log(String name, String stringifiedValue)
{
  if(!initialized){
    return;
  }
  SDMode();
  // TODO
}

void NetworkSensor::syncTimeNTP()
{
  // to begin, shut down the server to free sockets
  // (ok because this function is called very infrequently and doesn't take
  // a significant amount of time)
  server.available().stop();
  {
    EthernetUDP Udp;
    Udp.begin(8888);
    IPAddress ntpServer(132, 163, 4, 101);
    const int PACKET_SIZE = 48;
    byte packetBuffer[PACKET_SIZE];
    /////////////////////
    // SEND UDP PACKET //
    /////////////////////
    Serial.println("Sending NTP packet");
    while (Udp.parsePacket() > 0) ; // discard any previously received packets
    // set all bytes in the buffer to 0
    memset(packetBuffer, 0, PACKET_SIZE);
    // Initialize values needed to form NTP request
    // (see URL above for details on the packets)
    packetBuffer[0] = 0b11100011;   // LI, Version, Mode
    packetBuffer[1] = 0;     // Stratum, or type of clock
    packetBuffer[2] = 6;     // Polling Interval
    packetBuffer[3] = 0xEC;  // Peer Clock Precision
    // 8 bytes of zero for Root Delay & Root Dispersion
    packetBuffer[12]  = 49;
    packetBuffer[13]  = 0x4E;
    packetBuffer[14]  = 49;
    packetBuffer[15]  = 52;
    // all NTP fields have been given values, now
    // you can send a packet requesting a timestamp:                 
    Udp.beginPacket(ntpServer, 123); // NTP protocol uses port 123
    Udp.write(packetBuffer, PACKET_SIZE);
    Udp.endPacket();
    ///////////////////
    // READ RESPONSE // 
    ///////////////////
    Serial.println("Reading response");
    unsigned long beginWait = millis();
    // wait a full 1500 milliseconds before giving up on response
    while (millis() - beginWait < 1500UL) {
      int size = Udp.parsePacket();
      if (size >= PACKET_SIZE) {
        Serial.println("Received NTP Data");
        Udp.read(packetBuffer, PACKET_SIZE);  // read packet into the buffer
        unsigned long secsSince1900;
        // convert four bytes starting at location 40 to a long integer
        secsSince1900 =  (unsigned long)packetBuffer[40] << 24;
        secsSince1900 |= (unsigned long)packetBuffer[41] << 16;
        secsSince1900 |= (unsigned long)packetBuffer[42] << 8;
        secsSince1900 |= (unsigned long)packetBuffer[43];
        // NTP measures time in seconds since 1900
        // Unix measures time in seconds since 1970
        // There are 2208988800 seconds between 1900 and 1970.
        unsigned long epoch = secsSince1900 - 2208988800UL;
        setTime(epoch);
        last_time_sync = millis();
      } else{
        //Serial.print("packet size: ");
        //Serial.println(size);
      }
    }
  }
  //Serial.println("NTP transaction done!");
  server.begin();
}