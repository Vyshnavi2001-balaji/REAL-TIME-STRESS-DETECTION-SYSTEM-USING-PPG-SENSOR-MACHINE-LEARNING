#include "Arduino_LED_Matrix.h" // Official Arduino R4 onboard LED matrix library
#define PPG_PIN A0

const int LED = LED_BUILTIN; 
ArduinoLEDMatrix matrix;

// Define face patterns as byte arrays (8 rows × 12 columns)
byte happy[8][12] = {
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,1,0,0,0,0,0,0,1,0,0},
  {0,1,0,1,0,0,0,0,1,0,1,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,1,1,1,1,1,1,1,1,0,0},
  {0,1,0,0,0,0,0,0,0,0,1,0},
  {0,0,1,1,1,1,1,1,1,1,0,0}
};

byte sad[8][12] = {
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,1,0,0,0,0,0,0,1,0,0},
  {0,1,0,1,0,0,0,0,1,0,1,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,1,1,1,1,1,1,1,1,0,0},
  {0,1,0,0,0,0,0,0,0,0,1,0}
};

void setup() {
  Serial.begin(115200);
  matrix.begin();
  matrix.clear();
}


void loop() {
  int ppgValue = analogRead(PPG_PIN);
  Serial.println(ppgValue);
  delay(50);  // ~20Hz
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == "CALM") {
      Serial.println(" Showing Happy Face");
      matrix.renderBitmap(happy, 8, 12);
    } else if (msg == "STRESS") {
      Serial.println(" Showing Sad Face");
      matrix.renderBitmap(sad, 8, 12);
    }
  }
}
