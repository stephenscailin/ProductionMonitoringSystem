const int sensorPin = 2;

int lastSensorState = LOW;   // PNP: idle is LOW

void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
  Serial.println("Sensor test started");
}

void loop() {
  int currentState = digitalRead(sensorPin);

  // PNP: beam blocked = pin goes HIGH
  if (currentState == HIGH && lastSensorState == LOW) {
    Serial.println("PART DETECTED");
  }

  lastSensorState = currentState;
  delay(20);
}