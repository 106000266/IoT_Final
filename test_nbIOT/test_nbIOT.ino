#include <SoftwareSerial.h>

SoftwareSerial AT(8,9);
char val;

void setup()
{
  Serial.begin(9600);
  Serial.println("AT is ready!");
  AT.begin(9600);
}

void loop()
{
  if(Serial.available())
  {
    val = Serial.read();
    Serial.flush();
    AT.print(val);
  }

  if(AT.available())
  {
    val = AT.read();
    Serial.print(val);
    Serial.flush();
  }
}
