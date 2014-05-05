#include "NetworkSensor.h"

NetworkSensor::NetworkSensor(char** strings, int nstrings, char** floats, int nfloats, char** ints, int nints)
: initialized(false), server(SERVERPORT)
{
  for(int i=0; i<nstrings; ++i) logs(strings[i], "");
  for(int i=0; i<nfloats; ++i)  logf(floats[i], 0.0);
  for(int i=0; i<nints; ++i)    logs(ints[i], 0);
}

NetworkSensor::~NetworkSensor(){}

void NetworkSensor::begin(uint8_t mac[], uint8_t ip[])
{
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
const char* quote = "\"";
const char* quote_colon_brace_t_colon = "\":{\"t\":";
const char* comma_v_colon = ",\"v\":";
const char* rbrace_comma = "},";
const char* rbrace_end = "}";

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
    typedef enum readstate{UNREAD, READING, DONE} readstate;
    readstate reading = UNREAD;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        // the header for the request should look like "GET / HTTP/1.1"
        // if it's boring, or "GET /1358283494 HTTP/1.1" if it is providing
        // us with an epoch time. here we parse that time by looking for the
        // first instance of '/'

        // condition to start reading epoch argument:
        if(reading == UNREAD && c == '/'){
          reading = READING;
          continue;
        }
        if(reading == READING){
          // condition to continue adding digits to epoch argument:
          if('0' <= c && c <= '9'){
            epoch_arg = epoch_arg*10+c-'0';
          // condition to finish reading and set time
          } else{
            reading = DONE;
            if(epoch_arg > 0) remoteSetTime(epoch_arg);
          }
        } 

        int total_lines = s_values.size + f_values.size + i_values.size;
        int line = 1; // this is used to ensure that the last entry has no trailing comma

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
            for(int i=0; i<s_values.size; ++i, ++line){
              client.print(quote);                      // "
              client.print(s_values.names[i]);          // name
              client.print(quote_colon_brace_t_colon);  // ":{"t":
              client.print(String(s_values.times[i]));  // time
              client.print(comma_v_colon);              // ,"v":
              client.print(quote);                      // "
              client.print(s_values.values[i]);         // value
              client.print(quote);                      // "
              client.println(line < total_lines ? rbrace_comma : rbrace_end);             // }, OR }
            }
            for(int i=0; i<f_values.size; ++i, ++line){
              client.print(quote);                                    // "
              client.print(f_values.names[i]);                        // name
              client.print(quote_colon_brace_t_colon);                // ":{"t":
              client.print(String(f_values.times[i]));                // time
              client.print(comma_v_colon);                            // ,"v":
              client.print(floatToString(f_values.values[i], 10000)); // v.alue
              client.println(line < total_lines ? rbrace_comma : rbrace_end);                           // }, OR }
            }
            for(int i=0; i<i_values.size; ++i, ++line){
              client.print(quote);                      // "
              client.print(i_values.names[i]);          // name
              client.print(quote_colon_brace_t_colon);  // ":{"t":
              client.print(String(i_values.times[i]));  // time
              client.print(comma_v_colon);              // ,"v":
              client.print(String(i_values.values[i])); // value
              client.println(line < total_lines ? rbrace_comma : rbrace_end);             // }, OR }
            }
          }
          client.println(rbrace);
          
          break;
        }
        currentLineIsBlank = (c == '\n' || c == '\r');
      }
    }
    delay(10);
    client.stop();
  }
}

void NetworkSensor::remoteSetTime(time_t epoch_seconds){
  // note that we need to work in seconds rather than milliseconds because
  // that is the difference between needing 32- and 64-bit integers
  time_t new_offset = epoch_seconds - (millis() / 1000);
  // update existing times
  time_t update = new_offset - s_values.offset_seconds; // this is zero if the clocks are synced
  for(int i=0; i<s_values.size; ++i) s_values.times[i] += update;
  for(int i=0; i<f_values.size; ++i) f_values.times[i] += update;
  for(int i=0; i<i_values.size; ++i) i_values.times[i] += update;
  s_values.offset_seconds = new_offset;
  f_values.offset_seconds = new_offset;
  i_values.offset_seconds = new_offset;
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
