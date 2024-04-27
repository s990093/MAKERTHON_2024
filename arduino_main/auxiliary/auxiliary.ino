const int LEDRow = 10;
const int buzzerPin = 13;
const int InPin = 12;
const int testPin = A0;

// 定義每個 LED 的引腳
//int ledPins[LEDRow] = {11, 10, 9, 8, 7, 6, 5, 4, 3, 2};
int ledPins[LEDRow] = {10, 9, 8, 7, 6, 5, 4, 3, 2};

// 用於檢測信號變化
bool click(bool signal);

// 執行 LED 點亮序列的函數
void runLedSequence() {
  for (int row = 0; row < LEDRow; row++) {
    digitalWrite(ledPins[row], HIGH); // 點亮 LED
    delay(150); // 延遲 150 毫秒
    digitalWrite(ledPins[row], LOW); // 關掉 LED
  }
}

void setup() {
  pinMode(InPin, INPUT);
  pinMode(testPin, INPUT);
  Serial.begin(115200);
  Serial.println("test!");

  // 初始化 LED 為輸出模式
  for (int row = 0; row < LEDRow; row++) {
    pinMode(ledPins[row], OUTPUT);
  }
}

void loop() {
  delay(100);
  // if (digitalRead(testPin) == 1) { // 檢查 testPin
  if (0) { // 檢查 testPin
    Serial.println("test mod");
    int receivedSignal = digitalRead(InPin);
    if (receivedSignal == 1) {
      runLedSequence(); // 執行 LED 點亮序列
    }
  } else {
    // 使用 click 函數檢測 InPin 的信號變化
      if (click(digitalRead(InPin))) {
        Serial.println("run mod");
        runLedSequence(); // 執行 LED 點亮序列
        runLedSequence(); // 執行 LED 點亮序列
      }else{
        Serial.println("temp mod");
      }
  }
}

// 點擊檢測函數，用於檢測信號的上升沿
bool click(bool signal) {
  static bool oldState = signal;
  static bool newState;
  bool result = false;
  newState = signal;

  if (newState == 1 && oldState == 0) {
    result = true; // 檢測到信號上升沿
  }

  oldState = newState; // 更新舊的狀態

  return result;
}