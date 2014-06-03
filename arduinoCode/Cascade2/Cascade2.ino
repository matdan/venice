/*
  SerialSweepN
  Reads serial data until the null byte and turns that data into servo movement for n servos

  Note: Change numServos to number of servos and set servoPins to correct pins
*/
#include <Servo.h> 

//int servoPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25};
int servoPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,16, 19, 20, 21, 22, 23, 24, 25,26,27,28}; //servoArduino3
const int numServos = sizeof(servoPins)/sizeof(int);
Servo servos[numServos];

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

char serialData[numServos * 3];
char tempData[3];

void setup() {
  // initialize serial:
  Serial.begin(9600);
  Serial.println("Ready");
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  for (int i=0; i < numServos; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90);
  }
}

void loop() {
  if (stringComplete) {
    for (int i=0; i < numServos; i++) {
      int value = inputString.substring(i*3, i*3+3).toInt();
      servos[i].write(value);
    }
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '/n') {
      stringComplete = true;
      break;
    } 
    // add it to the inputString:
    inputString += inChar;
  }
}
