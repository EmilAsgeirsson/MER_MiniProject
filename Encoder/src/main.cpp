#include <Arduino.h>

// Define float_t as float
using float_t = float;

void setup()
{
  delay(1000);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  pinMode(PIN_A0, INPUT);
  pinMode(PIN_A1, INPUT);
  pinMode(PIN_A2, INPUT);

  Serial.begin(115200);
  Serial.print("System ready\n");
}

constexpr float_t to_angle = 270.0F / 1023.0F;
constexpr uint8_t decimals = 2;

void loop()
{
  // Read the analog values
  const float_t value_a0 = analogRead(PIN_A0);
  const float_t value_a1 = analogRead(PIN_A1);
  const float_t value_a2 = analogRead(PIN_A2);

  // Calculate the values
  const float_t bar = (value_a0 > 101) ? 0.0131F * value_a0 - 1.326 : 0.0F;
  const float_t angle_1 = value_a1 * to_angle;
  const float_t angle_2 = value_a2 * to_angle;

  // Print the values
  Serial.print(String(bar, decimals) + ',' +
               String(angle_1, decimals) + ',' +
               String(angle_2, decimals) + '\n');
}