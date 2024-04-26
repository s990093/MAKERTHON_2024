#include "util.h"

int lastButtonState = HIGH; 
int buttonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

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
  digitalWrite(pinLed,mode); 
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
  // Serial.println(data);
  int httpCode = http.POST(data);
  if (httpCode > 0) {
    String payload = http.getString();
    // Serial.println("HTTP POST request successful");
    // Serial.println("Response: " + payload);
  } else {
    String temp = http.errorToString(httpCode).c_str();  // 获取HTTP错误信息
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
    // Serial.println("HTTP GET request successful");
    // Serial.println("Response: " + payload);
    // 解析JSON响应
    DynamicJsonDocument doc(256); 
    DeserializationError error = deserializeJson(doc, payload);
    // 检查是否解析成功
    if (error) {
      Serial.print("JSON解析失败: ");
      Serial.println(error.c_str());
      return;
    }
    // 提取变量的值
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
  int reading = digitalRead(pin);
  
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;

      if (buttonState == LOW) {
        Serial.println("Button pressed.");
        if(MainMode == 0) MainMode = 1;
        else MainMode = 0;
      }
    }
  }
  lastButtonState = reading;
}
