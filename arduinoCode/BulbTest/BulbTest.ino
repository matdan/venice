int bulbPins[] = {4, 5, 6, 8, 9, 10};
const int numBulbs = sizeof(bulbPins)/sizeof(int);

void setup() {
  for (int i=0; i<numBulbs; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  for (int i=0; i<numBulbs; i++) {
    digitalWrite(i, HIGH);
  }
}
