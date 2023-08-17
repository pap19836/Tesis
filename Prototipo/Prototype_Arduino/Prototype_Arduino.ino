#include <ESP32_Servo.h>
#include <ArduinoJson.h>
Servo servo1;
int servoPin1 = 22;
Servo servo2;
int servoPin2 = 23;

StaticJsonDocument<512> doc;

void setup() {
  //Initialize serial
  Serial.begin(9600); 
  while(!Serial) {
  }

  // Attach servos
  servo1.attach(servoPin1, 500, 2400); // min/max Ton 500us 2400us for sg90
  servo2.attach(servoPin2, 500, 2400);

  //debug led
  pinMode(21,OUTPUT);
}

void loop() {
  int pos1;
  int pos2;
  exchangeJSON();
  pos1 = int(doc["servo1"]);
  servo1.write(pos1);
  pos2 = int(doc["servo2"]);
  servo2.write(pos2);
  delay(100);
}

void exchangeJSON(){
  String  payload;
  while ( !Serial.available()  ){}
    if ( Serial.available() )
      payload = Serial.readStringUntil( '\n' );

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
