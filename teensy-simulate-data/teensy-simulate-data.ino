unsigned int FC = 0; // 16 bit unsigned
const unsigned int SYNC = 0xFC03; // What is optimal??
unsigned short int TEMP = 12; // 8 bit unsigned
unsigned short int PRES = 101; // 8 bit unsigned
unsigned int LAT = 69; // 16 bit unsigned
unsigned int LONG = 16; // 16 bit unsigned
unsigned short int ALT = 2; // 8 bit unsigned
unsigned short int IMG1 = 100; // 8 bit unsigned
unsigned short int IMG2 = 180; // 8 bit unsigned

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  char buffer_optimal[13*8];
  sprintf(buffer_optimal, "%04X%04X%02X%02X%02X%02X%02X%02X%02X", SYNC, FC, TEMP, PRES, LAT, LONG, ALT, IMG1, IMG2);

  Serial.print(buffer_optimal);
  delay(10);
  FC += 1;
  FC = FC % 65535;
}
