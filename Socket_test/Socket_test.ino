#include <WiFi.h>
 
const char* ssid = "HONOR Magic5 Lite 5G";
const char* password =  "2eqfy93cq4awwvp";

WiFiServer wifiServer(8091);

const uint16_t port = 8091;
void setup()
{
 
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  wifiServer.begin();
  
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
 
}

void loop() {
 
  WiFiClient client = wifiServer.available();
 
  if (client) {
 
    while (client.connected()) {
 
      while (client.available()>0) {
        char c = client.read();
        Serial.write(c);
      }
 
      delay(10);
    }
 
    client.stop();
    Serial.println("Client disconnected");
 
  }
}
