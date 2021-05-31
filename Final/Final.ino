#include <Arduino_FreeRTOS.h>

#include "ESP8266.h"
#include <SoftwareSerial.h> 

SoftwareSerial AT(8, 9); // Rx, Tx
ESP8266 wifi(AT);

#define SSID        "Dino"
#define PASSWORD    "dino1998"
#define HOST_NAME   "192.168.0.100"
#define HOST_PORT   (16628)

const int TriggerPin = 3;
const int EchoPin = 2;
long Duration = 0;

void setup()
{
  pinMode(TriggerPin, OUTPUT);
  pinMode(EchoPin, INPUT);
  Serial.begin(9600);
  
  Serial.println(wifi.getAPList().c_str());
  
  if (wifi.joinAP(SSID, PASSWORD)) {
        Serial.print("Join AP success\r\n");
        Serial.print("IP:");
        Serial.println( wifi.getLocalIP().c_str());       
    } else {
        Serial.print("Join AP failure\r\n");
    }
    
    if (wifi.disableMUX()) {
        Serial.print("single ok\r\n");
    } else {
        Serial.print("single err\r\n");
    }

    /*if (wifi.createTCP(HOST_NAME, HOST_PORT)) {
        Serial.print("create tcp ok\r\n");
    } else {
        Serial.print("create tcp err\r\n");
    }*/
}

void loop()
{ 
  digitalWrite(TriggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(TriggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(TriggerPin, LOW);

  Duration = pulseIn(EchoPin, HIGH);

  long Distance_cm = (Duration * 0.034) / 2;
  
  Serial.print("Distance: ");
  Serial.print(Distance_cm);
  Serial.println(" cm");
  delay(1000);
}
