#include <WiFi.h>
#include <ESP32_Servo.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <esp_pm.h>
#include <esp_wifi.h>
#include <esp_wifi_types.h>
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
Servo 8 = RightShoulder1
Servo 7 = LeftShoulder1
Servo 9 = RightShoulder2
Servo 6 = LeftShoulder2
*/
const char* ssid = "HONOR Magic5 Lite 5G";
const char* password =  "2eqfy93cq4awwvp";
const uint16_t port = 8091;

WiFiServer wifiServer(port);
StaticJsonDocument<4096> doc;
JsonArray LeftShoulder1 = doc["LeftShoulder1"];
JsonArray LeftShoulder2 = doc["LeftShoulder2"];
JsonArray LeftWaist = doc["LeftWaist"];
JsonArray LeftHip1 = doc["LeftHip1"];
JsonArray LeftHip2 = doc["LeftHip2"];
JsonArray LeftKnee = doc["LeftKnee"];
JsonArray LeftAnkle1 = doc["LeftAnkle1"];
JsonArray LeftAnkle2 = doc["LeftAnkle2"];
JsonArray RightShoulder1 = doc["RightShoulder1"];
JsonArray RightShoulder2 = doc["RightShoulder2"];
JsonArray RightWaist = doc["RightWaist"];
JsonArray RightHip1 = doc["RightHip1"];
JsonArray RightHip2 = doc["RightHip2"];
JsonArray RightKnee = doc["RightKnee"];
JsonArray RightAnkle1 = doc["RightAnkle1"];
JsonArray RightAnkle2 = doc["RightAnkle2"];

float servoValues[] ={90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90};
float coreo;
float coreo2;

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwmLegs = Adafruit_PWMServoDriver(0x40);
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40, Wire);

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

float US2Deg ( int us )
{
  float tasa_conv = ((USMAX - USMIN)/180);
  float ans = (us - USMIN)/tasa_conv;
  
  return(ans);
}


// You can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. It's not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= SERVO_FREQ;   // Analog servos run at ~60 Hz updates
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert input seconds to us
  pulse /= pulselength;
  Serial.println(pulse);
  pwmLegs.setPWM(n, 0, pulse);
}



void setup()
{
  Serial.begin(9600);
  Serial.println("8 channel Servo test!");

  pwmLegs.begin();
  /*
   * In theory the internal oscillator (clock) is 25MHz but it really isn't
   * that precise. You can 'calibrate' this by tweaking this number until
   * you get the PWM update frequency you're expecting!
   * The int.osc. for the PCA9685 chip is a range between about 23-27MHz and
   * is used for calculating things like writeMicroseconds()
   * Analog servos run at ~50 Hz updates, It is importaint to use an
   * oscilloscope in setting the int.osc frequency for the I2C PCA9685 chip.
   * 1) Attach the oscilloscope to one of the PWM signal pins and ground on
   *    the I2C PCA9685 chip you are setting the value for.
   * 2) Adjust setOscillatorFrequency() until the PWM update frequency is the
   *    expected value (50Hz for most ESCs)
   * Setting the value here is specific to each individual I2C PCA9685 chip and
   * affects the calculations for the PWM update frequency. 
   * Failure to correctly set the int.osc value will cause unexpected PWM results
   */
  pwmLegs.setOscillatorFrequency(27000000);
  pwmLegs.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

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

      String values;
      while (client.available()>0) {
        char c = client.read();
        values += c;
      }
      if(values != NULL){
        deserializeJson(doc, values);
        //exchangeJSON(values);
        
        if (!doc["uploadCoreo"]){
          Serial.printf("RW=%.3f RH1=%.3f RH2=%.3f RK=%.3f RA1=%.3f RA2=%.3f LW=%.3f LH1=%.3f LH2=%.3f LK=%.3f LA1=%.3f LA2=%.3f\n",
                       float((doc["RightWaist"])), float((doc["RightHip1"])), float((doc["RightHip2"])), float((doc["RightKnee"])), float((doc["RightAnkle1"])), float((doc["RightAnkle2"])),
                       float((doc["LeftWaist"])), float((doc["LeftHip1"])), float((doc["LeftHip2"])), float((doc["LeftKnee"])), float((doc["LeftAnkle1"])), float((doc["LeftAnkle2"])));
          servoValues[11] = float((doc["RightAnkle2"]));
          servoValues[9] = float((doc["RightAnkle1"]));
          servoValues[7] = float((doc["RightKnee"]));
          servoValues[5] = float((doc["RightHip2"]));
          servoValues[3] = float((doc["RightHip1"]));
          servoValues[1] = float((doc["RightWaist"]));

          servoValues[10] = float((doc["LeftAnkle2"]));
          servoValues[8] = float((doc["LeftAnkle1"]));
          servoValues[6] = 180-float((doc["LeftKnee"]));
          servoValues[4] = float((doc["LeftHip2"]));
          servoValues[2] = float((doc["LeftHip1"]));
          servoValues[0] = float((doc["LeftWaist"]));
        }

        else if(doc["uploadCoreo"]){
          LeftShoulder1 = doc["LeftShoulder1"];
          LeftShoulder2 = doc["LeftShoulder2"];
          LeftWaist = doc["LeftWaist"];
          LeftHip1 = doc["LeftHip1"];
          LeftHip2 = doc["LeftHip2"];
          LeftKnee = doc["LeftKnee"];
          LeftAnkle1 = doc["LeftAnkle1"];
          LeftAnkle2 = doc["LeftAnkle2"];
          RightShoulder1 = doc["RightShoulder1"];
          RightShoulder2 = doc["RightShoulder2"];
          RightWaist = doc["RightWaist"];
          RightHip1 = doc["RightHip1"];
          RightHip2 = doc["RightHip2"];
          RightKnee = doc["RightKnee"];
          RightAnkle1 = doc["RightAnkle1"];
          RightAnkle2 = doc["RightAnkle2"];
        }
      }

      if (!doc["uploadCoreo"]){
        for(int i=0; i<=11; i++){
          pwmLegs.writeMicroseconds(i, Deg2US ( servoValues[i], true ));
        }
      }
      else if(!doc["uploadCoreo"]){
        for(int i=0; i<sizeof(LeftShoulder1); i++){
          for(int j=0; j<=11; j++){
            servoValues[11] = RightAnkle2[i];
            servoValues[9] = 180-float(RightAnkle1[i]);
            servoValues[7] = RightKnee[i];
            servoValues[5] = RightHip2[i];
            servoValues[3] = RightHip1[i];
            servoValues[1] = RightWaist[i];

            servoValues[10] = 180-float(LeftAnkle2[i]);
            servoValues[8] = LeftAnkle1[i];
            servoValues[6] = 180.0-float(LeftKnee[i]);
            servoValues[4] = float(LeftHip2[i]);
            servoValues[2] = LeftHip1[i];
            servoValues[0] = LeftWaist[i];
            pwmLegs.writeMicroseconds(j, Deg2US ( servoValues[j], true ));
          }
          delay(0.5);
        }
      }

    }
    client.stop();
    Serial.println("Client disconnected");
  }

  // for(int i=0; i<15; i++){
  //   pwmLegs.writeMicroseconds(i, Deg2US ( servoValues[i], true ));
  // }


}

void exchangeJSON(String payload){

  DeserializationError   error = deserializeJson(doc, payload);
  if (error) {
    Serial.println(error.c_str()); 
    return;
  }
}
