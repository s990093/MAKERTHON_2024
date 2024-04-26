/// util.h ///
#ifndef UTIL_H
#define UTIL_H

#include <ESP8266WiFi.h>
#include <SimpleDHT.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>


extern SimpleDHT11 dht11;

extern bool MainMode;
extern bool DEPL;
extern bool RainData;
extern int HumiData;
extern byte TempData;
extern byte SoilData;
extern bool controlValve;
extern bool autoDetect;
extern int tempMode;

const int button1Pin = 14;  
const int pinDHT11 = 16; 
const int pinRain = 5;
const int pinHumi = 4;
const int pinLed = 0;

void readSensorData();
void readSensorData2();
void Judge();
void PostRequest();
void GetRequest();
void handleButton(int pin);

#endif
/// util.h ///

