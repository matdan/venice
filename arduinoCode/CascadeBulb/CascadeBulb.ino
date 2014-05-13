int bulbPins[] = {4, 5, 6, 8, 9, 10, 14, 15, 16, 18, 19, 20, 22, 23, 24, 26, 27, 28, 30, 31, 32, 34, 35, 36, 38, 39, 40, 42, 43, 44};
const int numBulbs = sizeof(bulbPins)/sizeof(int);

char serialData[numBulbs * 3];
char tempData[3];

void setup() {
  Serial.begin(9600);
  Serial.println("Ready");
  for (int i=0; i < numBulbs; i++) {
    pinMode(bulbPins[i], OUTPUT); 
  }
}

void loop() {
  if (Serial.available()) {
    Serial.readBytesUntil('\0', serialData, numBulbs * 3);
    
    for (int i=0; i < numBulbs; i++) {
      memmove(tempData, serialData + i * 3, 3);
      if (atoi(tempData) == 2) {
          digitalWrite(bulbPins[i], HIGH);
      }
      else {
          digitalWrite(bulbPins[i], LOW);
      }
    }
     delay(15);
  }
}
