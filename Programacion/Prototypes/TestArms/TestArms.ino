#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h> 

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define USMIN  625 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2385 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

// called this way, it uses the default address 0x40
AsyncWebServer server(80);

Adafruit_MPU6050 mpu;

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(0x41);

// const char* ssid = "ARRIS-E1B2";
// const char* password = "2PM7H7602754";

const char* ssid = "robi21";
const char* password = "xdxdxdxd";

int sensor1 = 0; //FSR402 derecho
int sensor2 = 0; //FSR402 izquierdo

float sensor3 = 0; //MPU6050 ax
float sensor4 = 0; //MPU6050 ay
float sensor5 = 0; //MPU6050 az
float sensor6 = 0; //MPU6050 gx
float sensor7 = 0; //MPU6050 gy
float sensor8 = 0; //MPU6050 gz

int j = 0;         //Contador Coreografía
int vel = 95;      //Velocidad de movimiento (0-100)
int demo = 0;      //Modo de demostración

//                        0             1             2             3            4            5             6             7             8            9           10           11            12            13          14           15
float Desfase[16] = {(47.5-45.0), (145.0-145.0), (93.0-90.0), (101.0-90.0), (95.0-90.0), (97.0-90.0), (145.0-145.0), (45.5-45.0), (101.5-90.0), (92.5-90.0), (97.0-90.0), (96.0-90.0), (95.0-90.0), (95.0-90.0), (95.0-90.0), (90.0-90.0)};
//                    0      1      2      3     4      5     6      7     8      9    10     11                                                                                                                                      12(d_ext) (0.0)         13(d_int)        14(i_int)        15(i_ext) (180.0)
float FaseEnd[16] = {45+Desfase[0], 145.0+Desfase[1], 90.0+Desfase[2], 90.0+Desfase[3], 90.0+Desfase[4], 90.0+Desfase[5], 145.0+Desfase[6], 45.0+Desfase[7], 90.0+Desfase[8], 90.0+Desfase[9], 90.0+Desfase[10], 90.0+Desfase[11], 90.0+Desfase[12], 90.0+Desfase[13], 90.0+Desfase[14], 90.0+Desfase[15]};


//------------------------- FUNCIONES ADICIONALES -------------------------------------------------------

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

void handleRoot(AsyncWebServerRequest *request) {
  // Crea un objeto JSON
  StaticJsonDocument<200> jsonDoc;
  
  // Agrega los datos de los sensores al objeto JSON
  jsonDoc["sensor1"] = sensor1;
  jsonDoc["sensor2"] = sensor2;

  jsonDoc["sensor3"] = sensor3;
  jsonDoc["sensor4"] = sensor4;
  jsonDoc["sensor5"] = sensor5;

  jsonDoc["sensor6"] = sensor6;
  jsonDoc["sensor7"] = sensor7;
  jsonDoc["sensor8"] = sensor8;

  // Convierte el objeto JSON a una cadena de texto
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  
  // Agrega la cabecera "Access-Control-Allow-Origin" para permitir acceso desde cualquier origen
  AsyncWebServerResponse *response = request->beginResponse(200, "application/json", jsonString);
  response->addHeader("Access-Control-Allow-Origin", "*");
  request->send(response);
}



//------------------------- SET UP -------------------------------------------------------

void setup() {
  //INICIALIZACIÓN SERIAL---------------------------------------
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause until serial console opens

  //INICIALIZACIÓN PCA9685------------------------------------
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  delay(10);
  pwm2.begin();
  pwm2.setOscillatorFrequency(27000000);
  pwm2.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  delay(10);

  //COLOCAR AL ROBTO DE PIE PARA INICIAR
  pwm.writeMicroseconds(0, Deg2US ( FaseEnd[0], true ));
  pwm.writeMicroseconds(1, Deg2US ( FaseEnd[1], true ));
  pwm.writeMicroseconds(2, Deg2US ( FaseEnd[2], true ));
  pwm.writeMicroseconds(3, Deg2US ( FaseEnd[3], true ));
  pwm.writeMicroseconds(4, Deg2US ( FaseEnd[4], true ));
  pwm.writeMicroseconds(5, Deg2US ( FaseEnd[5], true ));
  pwm.writeMicroseconds(6, Deg2US ( FaseEnd[6], true )); 
  pwm.writeMicroseconds(7, Deg2US ( FaseEnd[7], true )); 
  pwm.writeMicroseconds(8, Deg2US ( FaseEnd[8], true ));
  pwm.writeMicroseconds(9, Deg2US ( FaseEnd[9], true ));
  pwm.writeMicroseconds(10, Deg2US ( FaseEnd[10], true ));
  pwm.writeMicroseconds(11, Deg2US ( FaseEnd[11], true ));
  delay(10);
  pwm2.writeMicroseconds(2, Deg2US ( FaseEnd[12], true ));
  pwm2.writeMicroseconds(3, Deg2US ( FaseEnd[13], true ));
  pwm2.writeMicroseconds(12, Deg2US ( FaseEnd[14], true ));
  pwm2.writeMicroseconds(13, Deg2US ( FaseEnd[15], true ));

  //INICIALIZACIÓN MPU6050--------------------------------------
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()){
    case MPU6050_RANGE_2_G:
      Serial.println("+-2G");
      break;
    case MPU6050_RANGE_4_G:
      Serial.println("+-4G");
      break;
    case MPU6050_RANGE_8_G:
      Serial.println("+-8G");
      break;
    case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
    case MPU6050_RANGE_250_DEG:
      Serial.println("+- 250 deg/s");
      break;
    case MPU6050_RANGE_500_DEG:
      Serial.println("+- 500 deg/s");
      break;
    case MPU6050_RANGE_1000_DEG:
      Serial.println("+- 1000 deg/s");
      break;
    case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
    case MPU6050_BAND_260_HZ:
      Serial.println("260 Hz");
      break;
    case MPU6050_BAND_184_HZ:
      Serial.println("184 Hz");
      break;
    case MPU6050_BAND_94_HZ:
      Serial.println("94 Hz");
      break;
    case MPU6050_BAND_44_HZ:
      Serial.println("44 Hz");
      break;
    case MPU6050_BAND_21_HZ:
      Serial.println("21 Hz");
      break;
    case MPU6050_BAND_10_HZ:
      Serial.println("10 Hz");
      break;
    case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  //INICIALIZACIÓN WiFi--------------------------------------
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
  Serial.println(WiFi.localIP());

  // Configurar rutas del servidor
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    handleRoot(request);
  });

  // Iniciar servidor web
  server.begin();
}

void loop() {
  // Actualizar el valor de los sensores solo si hay una conexión activa
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  if (WiFi.status() == WL_CONNECTED) {
    // Actualiza aquí los valores de tus sensores
    sensor1 = analogRead(A0);
    sensor2 = analogRead(A3);
    sensor3 = a.acceleration.x;
    sensor4 = a.acceleration.y;
    sensor5 = a.acceleration.z;
    sensor6 = g.gyro.x;
    sensor7 = g.gyro.y;
    sensor8 = g.gyro.z;
  }
  if(demo == 1)
  {
    switch (j)
    {
      case 0: 
        for (int paso = 0; paso<=(100-40);paso++)
        {
          pwm.writeMicroseconds(4, Deg2US ( FaseEnd[4]-paso, true ));
          pwm.writeMicroseconds(5, Deg2US ( FaseEnd[5]+paso, true ));
          pwm.writeMicroseconds(6, Deg2US ( FaseEnd[6]-(paso*1.5), true ));
          pwm.writeMicroseconds(7, Deg2US ( FaseEnd[7]+(paso*1.5), true ));
          pwm.writeMicroseconds(8, Deg2US ( FaseEnd[8]+(paso*0.75), true ));
          pwm.writeMicroseconds(9, Deg2US ( FaseEnd[9]-(paso*0.75), true ));
          delay(100-vel);
          if (paso==(100-40))
          {
            FaseEnd[4] = FaseEnd[4]-paso;
            FaseEnd[5] = FaseEnd[5]+paso;
            FaseEnd[6] = FaseEnd[6]-(paso*1.25);
            FaseEnd[7] = FaseEnd[7]+(paso*1.25);
            FaseEnd[8] = FaseEnd[8]+(paso*0.5);
            FaseEnd[9] = FaseEnd[9]-(paso*0.5);
          }

          if (float(float(paso)/float(100-42))<=0.2 || float(float(paso)/float(100-42))>=0.5)
          {
            vel = 80;
          }
          else
          {
            vel = 90;
          }
        }
        break;
      case 1: 
        for (int paso = 0; paso<=(120-100);paso++)
        {
          pwm.writeMicroseconds(2, Deg2US ( FaseEnd[2]+paso, true ));
          pwm.writeMicroseconds(3, Deg2US ( FaseEnd[3]+paso, true ));
          pwm.writeMicroseconds(10, Deg2US ( FaseEnd[10]+paso, true ));
          pwm.writeMicroseconds(11, Deg2US ( FaseEnd[11]+paso, true ));
          delay(100-vel);
          if (paso==(120-100))
          {
            FaseEnd[2] = FaseEnd[2]+paso;
            FaseEnd[3] = FaseEnd[3]+paso;
            FaseEnd[10] = FaseEnd[10]+paso;
            FaseEnd[11] = FaseEnd[11]+paso;
          }
          
          if (float(float(paso)/float(100-42))<=0.2 || float(float(paso)/float(100-42))>=0.7)
          {
            vel = 80;
          }
          else
          {
            vel = 90;
          }
        }
        break;

      case 2: 
        for (int paso = 0; paso<=(120-100);paso++)
        {
          pwm.writeMicroseconds(2, Deg2US ( FaseEnd[2]-paso, true ));
          pwm.writeMicroseconds(3, Deg2US ( FaseEnd[3]-paso, true ));
          pwm.writeMicroseconds(10, Deg2US ( FaseEnd[10]-paso, true ));
          pwm.writeMicroseconds(11, Deg2US ( FaseEnd[11]-paso, true ));
          delay(100-vel);
          if (paso==(120-100))
          {
            FaseEnd[2] = FaseEnd[2]-paso;
            FaseEnd[3] = FaseEnd[3]-paso;
            FaseEnd[10] = FaseEnd[10]-paso;
            FaseEnd[11] = FaseEnd[11]-paso;
          }
          
          if (float(float(paso)/float(100-42))<=0.2 || float(float(paso)/float(100-42))>=0.7)
          {
            vel = 80;
          }
          else
          {
            vel = 90;
          }
        }
        break;

      case 3: 
        for (int paso = 0; paso<=(100-40);paso++)
        {
          pwm.writeMicroseconds(4, Deg2US ( FaseEnd[4]+paso, true ));
          pwm.writeMicroseconds(5, Deg2US ( FaseEnd[5]-paso, true ));
          pwm.writeMicroseconds(6, Deg2US ( FaseEnd[6]+(paso*1.5), true ));
          pwm.writeMicroseconds(7, Deg2US ( FaseEnd[7]-(paso*1.5), true ));
          pwm.writeMicroseconds(8, Deg2US ( FaseEnd[8]-(paso*0.75), true ));
          pwm.writeMicroseconds(9, Deg2US ( FaseEnd[9]+(paso*0.75), true ));
          delay(100-vel);
          if (paso==(100-40))
          {
            FaseEnd[4] = FaseEnd[4]+paso;
            FaseEnd[5] = FaseEnd[5]-paso;
            FaseEnd[6] = FaseEnd[6]+(paso*1.5);
            FaseEnd[7] = FaseEnd[7]-(paso*1.5);
            FaseEnd[8] = FaseEnd[8]-(paso*0.75);
            FaseEnd[9] = FaseEnd[9]+(paso*0.75);
          }
          
          if (float(float(paso)/float(100-42))<=0.2 || float(float(paso)/float(100-42))>=0.7)
          {
            vel = 80;
          }
          else
          {
            vel = 95;
          }
        }
        break;
      
      // case '5':
      //   pwm.writeMicroseconds(2, Deg2US ( 120, true ));
      //   pwm.writeMicroseconds(10, Deg2US ( 80, true ));
      //   pwm.writeMicroseconds(7, Deg2US ( 135, true ));
      //   pwm.writeMicroseconds(8, Deg2US ( 120, true ));
      //   pwm.writeMicroseconds(6, Deg2US ( 90, true ));
      //   pwm.writeMicroseconds(4, Deg2US ( 42.5, true ));
    }

    j++;
    if (j>3)
    {
      j=0;
    }
    delay(1000);

  } 
}