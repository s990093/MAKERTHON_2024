#ifndef UTIL_H
#define UTIL_H

#include <ESP8266WiFi.h>
#include <SimpleDHT.h>
#include <ArduinoJson.h>

#include "config.h"

SimpleDHT11 dht11;

extern bool MainMode;
extern bool DEPL;
extern bool RainData;
extern int HumiData;
extern byte TempData;
extern byte SoilData;
extern bool controlValve;
extern bool autoDetect;
extern int tempMode;

void readSensorData();
void readSensorData2();
void Judge();
void PostRequest();
void GetRequest();
void handleButton(int pin);

#endif
