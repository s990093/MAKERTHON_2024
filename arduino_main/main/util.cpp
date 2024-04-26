/// util.cpp ///
#include "util.h"

SimpleDHT11 dht11;

bool MainMode = false;
bool DEPL = false;
bool RainData = false;
int HumiData = 0;
byte TempData = 0;
byte SoilData = 0;
bool controlValve = false;
bool autoDetect = false;
int tempMode = 0;

void readSensorData2(){
  RainData = !digitalRead(pinRain);
  HumiData = 1023 - analogRead(pinHumi);
}

void Judge(){
  Serial.println("===============");
  Serial.print("RAIN:");
  Serial.println(RainData);
  Serial.print("HUMI:");
  Serial.println(HumiData);
  Serial.print("led type:");
  bool mode = 0;
  if(tempMode == 3) mode = 0;
  if(tempMode == 2) mode = 0;
  if(tempMode == 0) mode = 1;
  if(tempMode == 1){
    if(RainData == 0) mode = 0;
    else mode = 1;
  } 
  if(MainMode == 1) mode = 0; 
  digitalWrite(pinLed, mode); 
  Serial.println(mode);
}

void readSensorData() {
  // 读取传感器数据
  int err;
  if ((err = dht11.read(pinDHT11, &TempData, &SoilData, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.print(err); Serial.println("SimpleDHT");
    return;
  }
}

void PostRequest() {
  HTTPClient http;
  WiFiClient client;
  String apiUrl = "http://49.213.238.75:8000/i/local";  
  http.begin(client, apiUrl);
  http.addHeader("Content-Type", "application/json");
  DynamicJsonDocument jsonDoc(256);  
  jsonDoc["humd"] = float(SoilData);
  jsonDoc["temp"] = float(TempData);
  jsonDoc["elev"] = 500.0;
  jsonDoc["pres"] = float(HumiData);
  String data;
  serializeJson(jsonDoc, data);
  int httpCode = http.POST(data);
  if (httpCode > 0) {
    String payload = http.getString();
  } else {
    String temp = http.errorToString(httpCode).c_str();  
    Serial.println("HTTP POST request failed. Error: " + temp);
  }
  http.end();
}

void GetRequest() {
  HTTPClient http;
  WiFiClient client;
  String apiUrl = "http://49.213.238.75:8000/i/setting";  
  http.begin(client, apiUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.GET();
  if (httpCode > 0) {
    String payload = http.getString();
    DynamicJsonDocument doc(256); 
    DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.print("JSON解析失败: ");
      Serial.println(error.c_str());
      return;
    }
    controlValve = doc["control_valve"];
    autoDetect = doc["auto_detect"];
    tempMode = int(controlValve) * 2 + int(autoDetect);
    Serial.print("control_valve: ");
    Serial.println(controlValve);
    Serial.print("auto_detect: ");
    Serial.println(autoDetect);
  } else {
    String temp = http.errorToString(httpCode).c_str(); 
    Serial.println("HTTP GET request failed. Error: " + temp);
  }
  http.end();
}

void handleButton(int pin) {
  Serial.println("要報改");
}
/// util.cpp ///
