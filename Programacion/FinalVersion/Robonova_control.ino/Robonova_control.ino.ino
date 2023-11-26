#include <WiFi.h>
#include <ESP32_Servo.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <esp_pm.h>
#include <esp_wifi.h>
#include <esp_wifi_types.h>

//#define DEBUG
// Listado de servos
/*
Servo 11 = RightAnkle2
Servo 10 = LeftAnkle2
Servo 9 = RightAnkle1
Servo 8 = LeftAnkle1
Servo 7 = RightKnee
Servo 6 = LeftKnee
Servo 5 = RightHip2
Servo 4 = LeftHip2
Servo 3 = RightHip1
Servo 2 = LeftHip1
Servo 1 = RightWaist
Servo 0 = LeftWaist
segunda placa
Servo 3 = RightShoulder1
Servo 12 = LeftShoulder1
Servo 2 = RightShoulder2
Servo 13 = LeftShoulder2
*/
//                        0             1             2             3            4            5             6             7             8            9           10           11        12     13    14    15
float Desfase[16] = {(47.5-45.0), (145.0-145.0), (93.0-90.0), (101.0-90.0), (95.0-90.0), (97.0-90.0), (145.0-145.0), (45.5-45.0), (101.5-90.0), (92.5-90.0), (97.0-90.0), (96.0-90.0), 175.0, 175.0, 0.0, 0.0};
//                    0      1      2      3     4      5     6      7     8      9    10     11               12(i_ext)    13(d_ext)    14(d_int)    15(i_int)
const char* ssid = "HONOR Magic5 Lite 5G";
const char* password =  "2eqfy93cq4awwvp";
const uint16_t port = 8091;

WiFiServer wifiServer(port);
DynamicJsonDocument doc(75000);
JsonArray LeftShoulder1 = doc["LeftShoulder1"];
float LeftShoulder1Array[200];
JsonArray LeftShoulder2 = doc["LeftShoulder2"];
float LeftShoulder2Array[200];
JsonArray LeftWaist = doc["LeftWaist"];
float LeftWaistArray[200];
JsonArray LeftHip1 = doc["LeftHip1"];
float LeftHip1Array[200];
JsonArray LeftHip2 = doc["LeftHip2"];
float LeftHip2Array[200];
JsonArray LeftKnee = doc["LeftKnee"];
float LeftKneeArray[200];
JsonArray LeftAnkle1 = doc["LeftAnkle1"];
float LeftAnkle1Array[200];
JsonArray LeftAnkle2 = doc["LeftAnkle2"];
float LeftAnkle2Array[200];

JsonArray RightShoulder1 = doc["RightShoulder1"];
float RightShoulder1Array[200];
JsonArray RightShoulder2 = doc["RightShoulder2"];
float RightShoulder2Array[200];
JsonArray RightWaist = doc["RightWaist"];
float RightWaistArray[200];
JsonArray RightHip1 = doc["RightHip1"];
float RightHip1Array[200];
JsonArray RightHip2 = doc["RightHip2"];
float RightHip2Array[200];
JsonArray RightKnee = doc["RightKnee"];
float RightKneeArray[200];
JsonArray RightAnkle1 = doc["RightAnkle1"];
float RightAnkle1Array[200];
JsonArray RightAnkle2 = doc["RightAnkle2"];
float RightAnkle2Array[200];

float servoValues[] ={90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90};
float servoValuesArms[] ={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
int coreoLen;

unsigned long old_millis;
unsigned long dt;
// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwmLegs = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwmArms = Adafruit_PWMServoDriver(0x41);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define USMIN  625 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2385 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates


int Deg2US ( float grados, bool USMin_bool )
{
  float tasa_conv = ((USMAX - USMIN)/180);
  int ans = tasa_conv*grados;
  if (USMin_bool)
  {
    ans = ans + USMIN;
  }  
  else
  {
    ans = ans;
  }
  
  return(ans);
}

void setup()
{
  Serial.begin(9600);
  Serial.println("8 channel Servo test!");

  pwmLegs.begin();
  pwmLegs.setOscillatorFrequency(27000000);
  pwmLegs.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  pwmArms.begin();
  pwmArms.setOscillatorFrequency(27000000);
  pwmArms.setPWMFreq(SERVO_FREQ);

  WiFi.mode (WIFI_STA);
  esp_wifi_set_ps(WIFI_PS_NONE);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  wifiServer.begin();
  
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

  delay(10);
}

void loop() {
  WiFiClient client = wifiServer.available();
  if (client) {
    Serial.println("Client Connected");
    while (client.connected()) {
      String c;
      while (client.available()>0) {
        c = client.readStringUntil(10);
        //client.flush();
      }
      if(c != NULL){
        deserializeJson(doc, c);
        if(!doc["playCoreo"]){
          if (!doc["uploadCoreo"]){

            #ifdef DEBUG
            Serial.printf("RS1=%.3f RS2=%.3f RW=%.3f RH1=%.3f RH2=%.3f RK=%.3f RA1=%.3f RA2=%.3f LS1=%.3f LS2=%.3f LW=%.3f LH1=%.3f LH2=%.3f LK=%.3f LA1=%.3f LA2=%.3f\n",
                        float((doc["RightShoulder1"])), float((doc["RightShoulder2"])), float((doc["RightWaist"])), float((doc["RightHip1"])), float((doc["RightHip2"])), float((doc["RightKnee"])), float((doc["RightAnkle1"])), float((doc["RightAnkle2"])),
                        float((doc["LeftShoulder1"])), float((doc["LeftShoulder2"])), float((doc["LeftWaist"])), float((doc["LeftHip1"])), float((doc["LeftHip2"])), float((doc["LeftKnee"])), float((doc["LeftAnkle1"])), float((doc["LeftAnkle2"])));
            #endif

            servoValuesArms[3] = 180 - float((doc["RightShoulder1"]));
            servoValuesArms[2] = float((doc["RightShoulder2"]));
            
            servoValues[11] = 180 - float((doc["RightAnkle2"])) + Desfase[11];
            servoValues[9] = 180 - float((doc["RightAnkle1"])) + Desfase[9];
            servoValues[7] = float((doc["RightKnee"])) + Desfase[7];
            servoValues[5] = float((doc["RightHip2"])) + Desfase[5];
            servoValues[3] = float((doc["RightHip1"])) + Desfase[3];
            servoValues[1] = float((doc["RightWaist"])) + Desfase[1];

            servoValuesArms[12] = float((doc["LeftShoulder1"]));
            servoValuesArms[13] = 180 - float((doc["LeftShoulder2"]));
            
            servoValues[10] = 180 - float((doc["LeftAnkle2"])) + Desfase[10];
            servoValues[8] = float((doc["LeftAnkle1"])) + Desfase[8];
            servoValues[6] = 180 - float((doc["LeftKnee"])) + Desfase[6];
            servoValues[4] = 180 - float((doc["LeftHip2"])) + Desfase[4];
            servoValues[2] = float((doc["LeftHip1"])) + Desfase[2];
            servoValues[0] = float((doc["LeftWaist"])) + Desfase[0];
            
            for(int i=0; i<=13; i++){
              pwmLegs.writeMicroseconds(i, Deg2US ( servoValues[i], true ));
              pwmArms.writeMicroseconds(i, Deg2US ( servoValuesArms[i], true ));
            }
          }

          else if(doc["uploadCoreo"]){
            LeftShoulder1 = doc["LeftShoulder1"];
            copyArray(LeftShoulder1, LeftShoulder1Array);
            LeftShoulder2 = doc["LeftShoulder2"];
            copyArray(LeftShoulder2, LeftShoulder2Array);
            LeftWaist = doc["LeftWaist"];
            copyArray(LeftWaist, LeftWaistArray);
            LeftHip1 = doc["LeftHip1"];
            copyArray(LeftHip1, LeftHip1Array);
            LeftHip2 = doc["LeftHip2"];
            copyArray(LeftHip2, LeftHip2Array);
            LeftKnee = doc["LeftKnee"];
            copyArray(LeftKnee, LeftKneeArray);
            LeftAnkle1 = doc["LeftAnkle1"];
            copyArray(LeftAnkle1, LeftAnkle1Array);
            LeftAnkle2 = doc["LeftAnkle2"];
            copyArray(LeftAnkle2, LeftAnkle2Array);

            RightShoulder1 = doc["RightShoulder1"];
            copyArray(RightShoulder1, RightShoulder1Array);
            RightShoulder2 = doc["RightShoulder2"];
            copyArray(RightShoulder2, RightShoulder2Array);
            RightWaist = doc["RightWaist"];
            copyArray(RightWaist, RightWaistArray);
            RightHip1 = doc["RightHip1"];
            copyArray(RightHip1, RightHip1Array);
            RightHip2 = doc["RightHip2"];
            copyArray(RightHip2, RightHip2Array);
            RightKnee = doc["RightKnee"];
            copyArray(RightKnee, RightKneeArray);
            RightAnkle1 = doc["RightAnkle1"];
            copyArray(RightAnkle1, RightAnkle1Array);
            RightAnkle2 = doc["RightAnkle2"];
            copyArray(RightAnkle2, RightAnkle2Array);
            coreoLen = doc["coreoLen"];
            
            
            
            
            doc["uploadCoreo"] = false;
            Serial.println("Coreography uploaded");
            Serial.println(int(doc["coreoLen"]));

            #ifdef DEBUG
            for(int i=0; i<coreoLen; i++){
              Serial.printf("RS1=%.3f RS2=%.3f RW=%.3f RH1=%.3f RH2=%.3f RK=%.3f RA1=%.3f RA2=%.3f LS1=%.3f LS2=%.3f LW=%.3f LH1=%.3f LH2=%.3f LK=%.3f LA1=%.3f LA2=%.3f\n",
                        float(RightShoulder1[i]), float(RightShoulder2[i]), float(RightWaist[i]), float(RightHip1[i]), float(RightHip2[i]), float(RightKnee[i]), float(RightAnkle1[i]), float(RightAnkle2[i]),
                        float(LeftShoulder1Array[i]), float(LeftShoulder2Array[i]), float(LeftWaistArray[i]), float(LeftHip1[i]), float(LeftHip2[i]), float(LeftKnee[i]), float(LeftAnkle1[i]), float(LeftAnkle2[i]));
            }
            #endif
          
          }
        }
      }

      if(doc["playCoreo"]){
        Serial.println(bool(doc["repeat"]));
        do{
          for(int i=0; i<coreoLen; i++){
            old_millis = millis();
            servoValuesArms[3] = 180 - float(RightShoulder1Array[i]);
            servoValuesArms[2] = float(RightShoulder2Array[i]);
            servoValues[11] = 180- float(RightAnkle2Array[i]) + Desfase[11];
            servoValues[9] = 180-float(RightAnkle1Array[i]) + Desfase[9];
            servoValues[7] = float(RightKneeArray[i]) + Desfase[7];
            servoValues[5] = float(RightHip2Array[i]) + Desfase[5];
            servoValues[3] = float(RightHip1Array[i]) + Desfase[3];
            servoValues[1] = float(RightWaistArray[i]) +  + Desfase[1];

            servoValuesArms[12] = float(LeftShoulder1Array[i]);
            servoValuesArms[13] = 180 - float(LeftShoulder2Array[i]);
            servoValues[10] = 180-float(LeftAnkle2Array[i]) + Desfase[10];
            servoValues[8] = float(LeftAnkle1Array[i]) + Desfase[8];
            servoValues[6] = 180.0-float(LeftKneeArray[i]) + Desfase[6];
            servoValues[4] = 180-float(LeftHip2Array[i]) + Desfase[4];
            servoValues[2] = float(LeftHip1Array[i]) + Desfase[2];
            servoValues[0] = float(LeftWaistArray[i]) + Desfase[0];
            for(int j=0; j<=13; j++){
              pwmLegs.writeMicroseconds(j, Deg2US ( servoValues[j], true ));
              pwmArms.writeMicroseconds(j, Deg2US ( servoValuesArms[j], true ));
            }
            
            #ifdef DEBUG
            Serial.println("Playing Coreo...");
            Serial.printf("RS1=%.3f RS2=%.3f RW=%.3f RH1=%.3f RH2=%.3f RK=%.3f RA1=%.3f RA2=%.3f LS1=%.3f LS2=%.3f LW=%.3f LH1=%.3f LH2=%.3f LK=%.3f LA1=%.3f LA2=%.3f\n",
                      float(RightShoulder1[i]), float(RightShoulder2[i]), float(RightWaist[i]), float(RightHip1[i]), float(RightHip2[i]), float(RightKnee[i]), float(RightAnkle1[i]), float(RightAnkle2[i]),
                      float(LeftShoulder1Array[i]), float(LeftShoulder2Array[i]), float(LeftWaistArray[i]), float(LeftHip1[i]), float(LeftHip2[i]), float(LeftKnee[i]), float(LeftAnkle1[i]), float(LeftAnkle2[i]));
            #endif

            if(coreoLen<20){
              delay(500);
            }
            else{
              
            }
            while (client.available()>0) {
              c = client.readStringUntil(10);
              client.flush();
            }
            if(c != NULL){
              deserializeJson(doc, c);
            }
          }
          dt = millis()-old_millis;
          //Serial.println(dt);
        } while(doc["repeat"]);
        doc["playCoreo"] = false;
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}