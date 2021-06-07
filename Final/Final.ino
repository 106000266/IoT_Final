#include <Arduino_FreeRTOS.h>

#include "ESP8266.h"
#include <SoftwareSerial.h>

SoftwareSerial AT(8, 9); // Rx, Tx
ESP8266 wifi(AT);

#define SSID        "Wen"
#define PASSWORD    "12345678"
#define HOST_NAME   "192.168.137.1"
#define HOST_PORT   (16628)

const int TriggerPin = 3;
const int EchoPin = 2;
int ledPin = 5;      // select the pin for the LED
long Duration = 0;
uint8_t buffer[64] = {0};
uint32_t len;
bool msg_sent = false;

void setup()
{
  pinMode(TriggerPin, OUTPUT);
  pinMode(EchoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
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

    if (wifi.createTCP(HOST_NAME, HOST_PORT)) {
        Serial.print("create tcp ok\r\n");
    } else {
        Serial.print("create tcp err\r\n");
    }
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

  String msg = String(Distance_cm);
  msg_sent = wifi.send((const uint8_t*)msg.c_str(), msg.length());

  String received_msg;
  buffer[64] = {0};
  len = wifi.recv(buffer, sizeof(buffer), 10000);

  if (len > 0) {
      Serial.print("Received:[");
      for(uint32_t i = 0; i < len; i++) {
          received_msg.concat((char)buffer[i]);
          Serial.print((char)buffer[i]);
      }
      Serial.print("]\r\n");
  }

  if (received_msg.indexOf('d') == -1) {
      digitalWrite(ledPin, HIGH);
  }
  else {
      digitalWrite(ledPin, LOW);
  }

  delay(5000);
}
