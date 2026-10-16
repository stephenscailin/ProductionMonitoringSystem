const int NUM_STATIONS = 5;
const int sensorPins[NUM_STATIONS] = {2, 3, 4, 5, 6};

const unsigned long DEBOUNCE_MS = 20;

int lastState[NUM_STATIONS];
unsigned long lastChange[NUM_STATIONS];

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < NUM_STATIONS; i++) {
    pinMode(sensorPins[i], INPUT);
    lastState[i] = digitalRead(sensorPins[i]);
    lastChange[i] = 0;
  }
}

void loop() {
  unsigned long now = millis();

  for (int i = 0; i < NUM_STATIONS; i++) {
    int state = digitalRead(sensorPins[i]);

    if (state != lastState[i] && (now - lastChange[i]) >= DEBOUNCE_MS) {
      lastChange[i] = now;
      lastState[i] = state;

      // PNP: beam blocked = pin goes HIGH = new part
      if (state == HIGH) {
        Serial.print(i + 1);
        Serial.println(",PART_DETECTED");
      }
    }
  }
}