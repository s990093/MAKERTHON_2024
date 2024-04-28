/// main.ino ///
#include "timer.h"
#include "util.h"
#include "func.h"

unsigned long TempTemp = 0;  
unsigned long DebugTemp = 0;  
unsigned long RequestTemp = 0;  
unsigned long ServerTemp = 0;
unsigned long BuzzTemp = 0;  
bool buzzstate = 0;

void setup() {
  Serial.begin(115200);  
  pinMode(LED_BUILTIN, OUTPUT); 
  pinMode(OUT, OUTPUT); 
  pinMode(Buzzpin, OUTPUT); 

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

  if(MS - TempTemp >= TempTime){
    Debounce(isClick);
    TempTemp = MS;
  }

  if (MS - ServerTemp >= ServerTime) {
    GetRequest();
    ServerTemp = MS;
  }

  if (MS - BuzzTemp >= BuzzTime) {
    if(BUZT == 1) {
      digitalWrite(Buzzpin,buzzstate);
      if(buzzstate == 1) buzzstate = 0;
      else buzzstate = 1;
    }
    else digitalWrite(Buzzpin,0);
    BuzzTemp = MS;

  }

}
/// main.ino ///

