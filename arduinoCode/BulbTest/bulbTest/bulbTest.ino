int bulbPins[] = {22, 23, 24, 26, 27, 28, 30, 31, 32, 34, 35, 36, 38, 39, 40, 42, 43, 44, 45};
const int numBulbs = sizeof(bulbPins)/sizeof(int);

char serialData[numBulbs * 3];
char tempData[3];

void setup() {
  for (int i=0; i < numBulbs; i++) {
    pinMode(bulbPins[i], OUTPUT); 
    digitalWrite(bulbPins[i], LOW);
  }
}

void loop() {
  for (int i=0; i < numBulbs; i++) {
    digitalWrite(bulbPins[i], HIGH);
    delay(1000);
    digitalWrite(bulbPins[i], LOW);
  }
}
