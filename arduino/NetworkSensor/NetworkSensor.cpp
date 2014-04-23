#include "NetworkSensor.h"

NetworkSensor::NetworkSensor()
: initialized(false), server(SERVERPORT)
{}

NetworkSensor::~NetworkSensor(){}

void NetworkSensor::begin(uint8_t mac[], uint8_t ip[])
{
  Serial.begin(9600); // for debugging
  // SS (Slave Select) pin low to enable ethernet
  pinMode(ETHSS, OUTPUT);
  digitalWrite(ETHSS, LOW);
  pinMode(SDSS, OUTPUT);
  digitalWrite(SDSS, HIGH);

  initEthernet(mac, ip);
}

// reduce memory footprint by keeping only one instance of each string
const char* lbrace = "{";
const char* rbrace = "}";
const char* colon_brace_t_colon = ":{t:";
const char* comma_v_colon = ",v:";
const char* rbrace_comma = "},";

void NetworkSensor::input_output()
{
  if(!initialized){
    return;
  }
  // check for client connections and write requested data back
  EthernetClient client = server.available();
  if (client) {
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    time_t epoch_arg = 0;
    boolean reading_epoch = false, read_epoch = false;
    char last_c = ' ';
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        // the header for the request should look like "GET / HTTP"
        // if it's boring, or "GET /1358283494 HTTP" if it is providing
        // us with an epoch time. here we parse that time.
        if(last_c == '/' && !read_epoch) reading_epoch = true;
        if(reading_epoch && '0' <= c && c <= '9'){
          epoch_arg = epoch_arg*10+c-'0';
        } else if(reading_epoch){
          read_epoch = true;
          reading_epoch = false;
          remoteSetTime(epoch_arg);
        }

        // if we've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so we can send a reply
        if (c == '\n' && currentLineIsBlank) {
          // send a standard http response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: application/json");
          client.println();

          client.println(lbrace);
          {
            for(int i=0; i<s_values.size; ++i){
              client.print(s_values.names[i]);
              client.print(colon_brace_t_colon); // ":{t:"
              client.print(String(s_values.times[i]));
              client.print(comma_v_colon); // ",v:"
              client.print(s_values.values[i]);
              client.println(rbrace_comma); // "},"
            }
            for(int i=0; i<f_values.size; ++i){
              client.print(f_values.names[i]);
              client.print(colon_brace_t_colon); // ":{t:"
              client.print(String(f_values.times[i]));
              client.print(comma_v_colon); // ",v:"
              client.print(floatToString(f_values.values[i], 1000));
              client.println(rbrace_comma); // "},"
            }
            for(int i=0; i<i_values.size; ++i){
              client.print(i_values.names[i]);
              client.print(colon_brace_t_colon); // ":{t:"
              client.print(String(i_values.times[i]));
              client.print(comma_v_colon); // ",v:"
              client.print(String(i_values.values[i]));
              client.println(rbrace_comma); // "},"
            }
          }
          client.println(rbrace);
          
          break;
        }
        currentLineIsBlank = (c == '\n' || c == '\r');
        last_c = c;
      }
    }
    delay(10);
    client.stop();
  }
}

void NetworkSensor::remoteSetTime(time_t epoch){
  Serial.print("time set to ");
  Serial.println(epoch);
  time_t new_offset = epoch - millis();
  // update existing times
  time_t update = new_offset - s_values.offset_millis; // this is zero if the clocks are synced
  for(int i=0; i<s_values.size; ++i) s_values.times[i] += update;
  for(int i=0; i<f_values.size; ++i) f_values.times[i] += update;
  for(int i=0; i<i_values.size; ++i) i_values.times[i] += update;
  s_values.offset_millis = new_offset;
  f_values.offset_millis = new_offset;
  i_values.offset_millis = new_offset;
}

void NetworkSensor::logf(String name, float value)
{
  f_values.set(name, value);
}

void NetworkSensor::logi(String name, int value)
{
  i_values.set(name, value);
}

void NetworkSensor::logs(String name, String value)
{
  s_values.set(name, value);
}

void NetworkSensor::initEthernet(uint8_t mac[], uint8_t ip[])
{
  // Server initialization
  IPAddress ip_addr(ip[0], ip[1], ip[2], ip[3]);
  Ethernet.begin(mac, ip_addr);
  server.begin();
  initialized = true;
}
