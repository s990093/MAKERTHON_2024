/// main.ino ///
#include "timer.h"
#include "util.h"
#include "func.h"

unsigned long DebugTemp = 0;  
unsigned long RequestTemp = 0;  
unsigned long ServerTemp = 0;

void setup() {
  Serial.begin(115200);  
  pinMode(LED_BUILTIN, OUTPUT); 
  wifi_inti("RU_A15","qaz654321");
}

void loop() {
  unsigned long MS = millis();

  if (MS - DebugTemp >= DebugTime) {
    HelloWorld();
    DebugTemp = MS;
  }

  // // Execute API request
  // if (MS - RequestTemp >= RequestTime) {
  //   PostRequest();
  //   RequestTemp = MS;
  // }


  if (MS - ServerTemp >= ServerTime) {
    GetRequest();
    ServerTemp = MS;
  }


}
/// main.ino ///

