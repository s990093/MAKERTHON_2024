/// func.cpp ///
#include "func.h"

bool DEPL;
bool isClick;
bool BUZT;

void PostRequest()
{
  HTTPClient http;
  WiFiClient client;
  String apiUrl = "http://49.213.238.75:8000/i/local";
  http.begin(client, apiUrl);
  http.addHeader("Content-Type", "application/json");
  DynamicJsonDocument jsonDoc(256);
  // jsonDoc["humd"] = float(SoilData);
  // jsonDoc["temp"] = float(TempData);
  // jsonDoc["elev"] = 500.0;
  // jsonDoc["pres"] = float(HumiData);
  String data;
  serializeJson(jsonDoc, data);
  int httpCode = http.POST(data);
  if (httpCode > 0)
  {
    String payload = http.getString();
  }
  else
  {
    String temp = http.errorToString(httpCode).c_str();
    Serial.println("HTTP POST request failed. Error: " + temp);
  }
  http.end();
}
// void GetRequest() {
//   HTTPClient http;
//   WiFiClient client;
//   String apiUrl = "http://49.213.238.75:8000/i/setting";
//   http.begin(client, apiUrl);
//   http.addHeader("Content-Type", "application/json");
//   int httpCode = http.GET();
//   if (httpCode > 0) {
//     String payload = http.getString();
//     DynamicJsonDocument doc(256);
//     DeserializationError error = deserializeJson(doc, payload);
//     if (error) {
//       Serial.print("JSON解析失败: ");
//       Serial.println(error.c_str());
//       return;
//     }
//     isClick = doc["isClick"];
//     Serial.print("isClick: ");
//     Serial.println(isClick);

//     // controlValve = doc["control_valve"];
//     // autoDetect = doc["auto_detect"];
//     // tempMode = int(controlValve) * 2 + int(autoDetect);
//     // Serial.print("control_valve: ");
//     // Serial.println(controlValve);
//     // Serial.print("auto_detect: ");
//     // Serial.println(autoDetect);

//   } else {
//     String temp = http.errorToString(httpCode).c_str();
//     Serial.println("HTTP GET request failed. Error: " + temp);
//   }
//   http.end();
// }
void GetRequest()
{
  HTTPClient http;
  WiFiClient client;
  String apiUrl = "http://49.213.238.75:8000/app/";
  http.begin(client, apiUrl);
  http.setTimeout(500); // 設置超時時間為 1000 毫秒
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.GET();
  if (httpCode > 0)
  {
    String payload = http.getString();
    DynamicJsonDocument doc(256);
    DeserializationError error = deserializeJson(doc, payload);
    if (error)
    {
      Serial.print("JSON解析失败: ");
      Serial.println(error.c_str());
      return;
    }
    isClick = doc["is_clicked"];
    Serial.print("isClick: ");
    Serial.println(isClick);
  }
  else
  {
    String temp = http.errorToString(httpCode).c_str();
    Serial.println("HTTP GET request failed. Error: " + temp);
  }
  http.end();
}

void HelloWorld()
{
  Serial.println("debug test");
  digitalWrite(LED_BUILTIN, DEPL);
  if (DEPL == 1)
    DEPL = 0;
  else
    DEPL = 1;
}

void Debounce(bool state)
{
  static bool oldState = state;
  static bool newState;
  BUZT = 0;
  newState = state;
  if (newState != oldState && newState == true)
  {
    Serial.println("彈跳！");
    BUZT = 1;
  }
  digitalWrite(OUT, BUZT);
  oldState = newState;
}

void Debounce2(bool state)
{
  static bool oldState = state;
  static bool newState;
  int mod = 0;
  newState = state;
  if (newState != oldState)
  {

    Serial.println("彈跳2！ " + newState);
    mod = newState;
    digitalWrite(OUT, mod);
  }
  oldState = newState;
}
/// func.cpp ///
