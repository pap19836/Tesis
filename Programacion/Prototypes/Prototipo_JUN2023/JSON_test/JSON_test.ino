#include <ArduinoJson.h>
void setup() {
  Serial.begin(9600); 
  while(!Serial) {
  }
  pinMode(23,OUTPUT);
}

void loop() {
  int     size_ = 0;
  String  payload;
  while ( !Serial.available()  ){}
  if ( Serial.available() )
    payload = Serial.readStringUntil( '\n' );
  StaticJsonDocument<512> doc;

  DeserializationError   error = deserializeJson( , payload);
  if (error) {
    Serial.println(error.c_str()); 
    return;
  }
  if (doc["servo1"] == "1") {
     Serial.println("{\"Success\":\"True\"}");
     digitalWrite(23,HIGH);
  }
  else {
      Serial.println("{\"Success\":\"False\"}");
      digitalWrite(23,LOW);
   }
  delay(20);
}
