#include <WiFi.h>
#include <ESP32_Servo.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//Servo servo1;
//int servoPin1 = 22;
//Servo servo2;
//int servoPin2 = 23;
// Listado de servos
/*
Servo 0 = RightAnkle2
Servo 1 = LeftAnkle2
Servo 2 = RightAnkle1
Servo 3 = LeftAnkle1
Servo 4 = RightKnee
Servo 5 = LeftKnee
Servo 6 = RightHip2
Servo 7 = LeftHip2
Servo 8 = RightHip1
Servo 9 = LeftHip1
Servo 10 = RightWaist
Servo 11 = LeftWaist
Servo 12 = RightShoulder1
Servo 13 = LeftShoulder1
Servo 14 = RightShoulder2
Servo 15 = LeftShoulder2
*/
const char* ssid = "HONOR Magic5 Lite 5G";
const char* password =  "2eqfy93cq4awwvp";
const uint16_t port = 8091;

WiFiServer wifiServer(port);

StaticJsonDocument<512> doc;

int servoValues[] ={90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90};


// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
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
  pwm.setPWM(n, 0, pulse);
}



void setup()
{
  Serial.begin(9600);
  Serial.println("8 channel Servo test!");

  pwm.begin();
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
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  wifiServer.begin();
  
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

/*
  // Attach servos
  servo1.attach(servoPin1, 500, 2400); // min/max Ton 500us 2400us for sg90
  servo2.attach(servoPin2, 500, 2400);

  //debug led
  pinMode(21,OUTPUT);
*/
  delay(10);
}

void loop() {
  WiFiClient client = wifiServer.available();
  if (client) {
    while (client.connected()) {

      String values;
      while (client.available()>0) {
        char c = client.read();
        values += c;
      }
      if(values != NULL){
        exchangeJSON(values);  
        Serial.println(int(doc["LeftShoulder1"]));
        //servo1.write(int(doc["LeftShoulder1"]));
        //servo2.write(int(doc["LeftShoulder2"]));
        servoValues[0] = int(doc["RightAnkle2"]);
        servoValues[1] = int(doc["LeftAnkle2"]);
        servoValues[2] = int(doc["RightAnkle1"]);
        servoValues[3] = int(doc["LeftAnkle1"]);
        servoValues[4] = int(doc["RightKnee"]);
        servoValues[5] = int(doc["LeftKnee"]);
        servoValues[6] = int(doc["RightHip2"]);
        servoValues[7] = int(doc["LeftHip2"]);
        servoValues[8] = int(doc["RightHip1"]);
        servoValues[9] = int(doc["LeftHip1"]);
        servoValues[10] = int(doc["RightWaist"]);
        servoValues[11] = int(doc["LeftWaist"]);
        servoValues[12] = int(doc["RightShoulder1"]);
        servoValues[13] = int(doc["LeftShoulder1"]);
        servoValues[14] = int(doc["RightShoulder2"]);
        servoValues[15] = int(doc["LeftShoulder2"]);
      }

      for(int i=0; i<15; i++){
        pwm.writeMicroseconds(i, Deg2US ( servoValues[i], true ));
      }

      delay(10);
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
  
  if (doc["LeftShoulder1"] == "50") {
     Serial.println("{\"Success\":\"True\"}");
     digitalWrite(21,HIGH);
  }
  else {
      Serial.println("{\"Success\":\"False\"}");
      digitalWrite(21,LOW);
   }
  delay(20);
}
