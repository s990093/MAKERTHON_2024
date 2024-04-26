#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#include "config.h"
#include "util.h"
#include "timer.h"

unsigned long DebugTemp = 0;  
unsigned long RequestTemp = 0;  
unsigned long BaseSensorTemp = 0;
unsigned long AdvancedSensorTemp = 0;
unsigned long ServerTemp = 0;

void setup() {
  WiFi.mode(WIFI_STA);
  Serial.begin(115200);  
  pinMode(LED_BUILTIN, OUTPUT); 
  pinMode(pinRain, INPUT);
  pinMode(pinHumi, INPUT);
  pinMode(pinLed, OUTPUT);
  pinMode(button1Pin, INPUT); 

  WiFi.begin(ssid, passphrase);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long MS = millis();
  handleButton(button1Pin);
  // Execute sensor reading
  if (MS - BaseSensorTemp >= BaseSensorTime) {
    readSensorData();
    BaseSensorTemp = MS;
  }

  // Execute API request
  if (MS - RequestTemp >= RequestTime) {
    PostRequest();
    RequestTemp = MS;
  }

  // Read rain sensor
  if (MS - AdvancedSensorTemp >= AdvancedSensorTime) {
    readSensorData2();
    AdvancedSensorTemp = MS;
  }

  if (MS - ServerTemp >= ServerTime) {
    GetRequest();
    Judge();
    ServerTemp = MS;
  }

  if (MS - DebugTemp >= DebugTime) {
    digitalWrite(LED_BUILTIN, DEPL);
    if (DEPL == 1) DEPL = 0;
    else DEPL = 1;
    DebugTemp = MS;
  }
}
