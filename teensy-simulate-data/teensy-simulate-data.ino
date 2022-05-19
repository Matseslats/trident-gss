unsigned int FC = 0; // 16 bit unsigned
const unsigned int SYNC = 0xFC03; // What is optimal??
unsigned short int TEMP = 12; // 8 bit unsigned
unsigned short int PRES = 101; // 8 bit unsigned
unsigned int LAT = 69; // 16 bit unsigned
unsigned int LONG = 16; // 16 bit unsigned
unsigned short int ALT = 2; // 8 bit unsigned
unsigned short int IMG1 = 100; // 8 bit unsigned
unsigned short int IMG2 = 180; // 8 bit unsigned

#include <GY91.h>

#include <Cansat_RFM96.h>
#define USE_SD 0

// Declare all variables
unsigned int counter = 0;
unsigned int counter2 = 0;

unsigned long _time = 0;
double ax, ay, az, gx, gy, gz, mx, my, mz, pressure;
GY91 gy91;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  if (!gy91.init()) {
    Serial.println("Could not initiate");
    while (1);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  gy91.read_acc();
  gy91.read_gyro();
  gy91.read_mag();
  PRES = gy91.readPressure();
  TEMP = gy91.readTemperature();

  ax = gy91.ax;
  ay = gy91.ay;
  az = gy91.az;

  gx = gy91.gx;
  gy = gy91.gy;
  gz = gy91.gz;

  mx = gy91.mx;
  my = gy91.my;
  mz = gy91.mz;
  char buffer_optimal[13*8];
  sprintf(buffer_optimal, "%04X%04X%02X%04X%02X%02X%02X%02X%02X", SYNC, FC, TEMP, PRES, LAT, LONG, ALT, IMG1, IMG2);

  Serial.print(buffer_optimal);
  delay(10);
  FC += 1;
  FC = FC % 65535;
}
