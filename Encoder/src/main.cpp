#include <Arduino.h>

void setup()
{
  delay(1000);

  pinMode(PIN_A0, INPUT);
  pinMode(PIN_A1, INPUT);
  pinMode(PIN_A2, INPUT);

  Serial.begin(115200);
  Serial.print("System ready\n");
}

constexpr float to_angle = 270.0F / 1023.0F;
constexpr uint8_t decimals = 2;

void loop()
{
  const float value_a0 = analogRead(PIN_A0); // Pressure
  const float value_a1 = analogRead(PIN_A1) * to_angle; // temp encoder
  const float value_a2 = analogRead(PIN_A2) * to_angle; // encoder
  Serial.print(String(value_a0, decimals) + ',' +
               String(value_a1, decimals) + ',' +
               String(value_a2, decimals) + '\n');
  delay(10);
}