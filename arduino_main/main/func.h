/// func.h ///
#ifndef FUNC_H
#define FUNC_H

#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#define OUT 14
#define Buzzpin 12


extern bool DEPL;
extern bool BUZT;

extern bool isClick;


void PostRequest();
void GetRequest();
void HelloWorld();
void Debounce(bool state);
void Debounce2(bool state);
#endif
/// func.h ///
