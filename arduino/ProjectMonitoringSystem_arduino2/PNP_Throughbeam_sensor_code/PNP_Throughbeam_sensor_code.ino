const int sensorPin = 2;

int lastSensorState = LOW;   // PNP idles LOW

void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT); // add external pull-down resistor if sensor isn't push-pull
  Serial.println("Sensor test started");
}

void loop() {
  int currentState = digitalRead(sensorPin);

  // Detect a new part entering the sensor
  if (currentState == HIGH && lastSensorState == LOW) {
    Serial.println("PART DETECTED");
  }

  // Remember previous state
  lastSensorState = currentState;

  delay(20);
}