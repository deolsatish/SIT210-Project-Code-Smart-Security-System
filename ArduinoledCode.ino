#include <Wire.h>
char c=0;
//const int ledPin = LED_BUILTIN;
const int ledPin = 8; 
static_assert(LOW == 0, "Expecting LOW to be 0");

void setup() {
  Wire.begin(0x8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(sendData);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // turn it off
}

void loop() {
  delay(100);
}
void sendData() {
  Wire.write(c);
}

// function that executes whenever data is received from rpi
// this function is registered as an event
void receiveEvent(int howMany) {
  while (Wire.available()) {
    c = Wire.read(); // receive byte as a character
    digitalWrite(ledPin, c);
    
    
  }
}
