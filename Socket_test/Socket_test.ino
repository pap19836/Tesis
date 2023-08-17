#include <WiFi.h>
#include <ESP32_Servo.h>
#include <ArduinoJson.h>

Servo servo1;
int servoPin1 = 22;
Servo servo2;
int servoPin2 = 23;

const char* ssid = "HONOR Magic5 Lite 5G";
const char* password =  "2eqfy93cq4awwvp";
const uint16_t port = 8091;

WiFiServer wifiServer(port);

StaticJsonDocument<512> doc;

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

  // Attach servos
  servo1.attach(servoPin1, 500, 2400); // min/max Ton 500us 2400us for sg90
  servo2.attach(servoPin2, 500, 2400);

  //debug led
  pinMode(21,OUTPUT);
}

void loop() {
  WiFiClient client = wifiServer.available();
  
  int pos1;
  int pos2;
  if (client) {
    while (client.connected()) {

      String values;
      while (client.available()>0) {
        char c = client.read();
        //Serial.write(c);
        values += c;
      }
      if(values != NULL){
        Serial.println(values);
        exchangeJSON(values);  
        servo1.write(int(doc["servo1"]));
        servo2.write(int(doc["servo2"]));
      }
      //pos1 = int(doc["servo1"]);
      //servo1.write(pos1);
      //pos2 = int(doc["servo2"]);
      //servo2.write(pos2);
      delay(100);
    }
    client.stop();
    Serial.println("Client disconnected");
  }

}

void exchangeJSON(String payload){

  DeserializationError   error = deserializeJson(doc, payload);
  if (error) {
    Serial.println(error.c_str()); 
    return;
  }
  
  if (doc["servo1"] == "50") {
     Serial.println("{\"Success\":\"True\"}");
     digitalWrite(21,HIGH);
  }
  else {
      Serial.println("{\"Success\":\"False\"}");
      digitalWrite(21,LOW);
   }
  delay(20);
}
