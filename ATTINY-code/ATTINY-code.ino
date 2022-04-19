#include <SoftwareSerial.h>

const byte rxRFMPin = 2;
const byte txRFMPin = 3;
const byte rxPiPin = 2;
const byte txPiPin = 3;

// Seriell port for RFM96
SoftwareSerial RFMSerial (rxRFMPin, txRFMPin);
// Seriell port for RFM96
SoftwareSerial RFMSerial (rxPiPin, txPiPin);

void setup() {
  // put your setup code here, to run once:
  RFMSerial.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (RFMSerial.available() > 0){
    
  }
}
