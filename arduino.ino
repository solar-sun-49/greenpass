#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd1(0x27, 16, 2);
LiquidCrystal_I2C lcd2(0x26, 16, 2);

int times[4];

void setup() {

  Serial.begin(9600);

  lcd1.init();
  lcd1.backlight();

  lcd2.init();
  lcd2.backlight();

  lcd1.clear();
  lcd2.clear();
}

void loop() {

  if (Serial.available()) {

    String data = Serial.readStringUntil('\n');

    sscanf(data.c_str(), "%d,%d,%d,%d",
           &times[0], &times[1], &times[2], &times[3]);

    runTrafficSystem();
  }
}

void displayLCD(int activeLane, int currentTimer) {

  // LCD 1
  lcd1.clear();

  // Lane 1
  lcd1.setCursor(0,0);

  if (activeLane == 0) {
    lcd1.print("L1 : GO ");
    lcd1.print(currentTimer);
    lcd1.print("s");
  }
  else {
    lcd1.print("L1 : STOP");
  }

  // Lane 2
  lcd1.setCursor(0,1);

  if (activeLane == 1) {
    lcd1.print("L2 : GO ");
    lcd1.print(currentTimer);
    lcd1.print("s");
  }
  else {
    lcd1.print("L2 : STOP");
  }


  // LCD 2
  lcd2.clear();

  // Lane 3
  lcd2.setCursor(0,0);

  if (activeLane == 2) {
    lcd2.print("L3 : GO ");
    lcd2.print(currentTimer);
    lcd2.print("s");
  }
  else {
    lcd2.print("L3 : STOP");
  }

  // Lane 4
  lcd2.setCursor(0,1);

  if (activeLane == 3) {
    lcd2.print("L4 : GO ");
    lcd2.print(currentTimer);
    lcd2.print("s");
  }
  else {
    lcd2.print("L4 : STOP");
  }
}

void runTrafficSystem() {

  for (int lane = 0; lane < 4; lane++) {

    for (int t = times[lane]; t >= 0; t--) {

      displayLCD(lane, t);

      delay(1000);
    }
  }
}
