/// func.h ///
#ifndef FUNC_H
#define FUNC_H

#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

extern bool MainMode;
extern bool DEPL;
extern bool RainData;
extern int HumiData;
extern byte TempData;
extern byte SoilData;
extern bool controlValve;
extern bool autoDetect;
extern int tempMode;

void PostRequest();
void GetRequest();
#endif
/// func.h ///
