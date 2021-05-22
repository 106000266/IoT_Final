#include <SoftwareSerial.h>
 
SoftwareSerial AT(8, 9); // Rx, Tx
char val;
 
void setup() {
  Serial.begin(9600);   // set buadrate between IDE and arduino
  Serial.println("AT is ready!");
 
  // set the buadrate of module
  AT.begin(9600);
}
 
void loop() {
  // If receive messege from IDE, send it to module
  if (Serial.available()) {
    val = Serial.read();
    Serial.flush();
    AT.print(val);
  }
 
  // If receive messege from module, display on IDE
  if (AT.available()) {
    val = AT.read();
    Serial.print(val);
    Serial.flush();
  }
}
