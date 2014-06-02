/*
  SerialSweepN
  Reads serial data until the null byte and turns that data into servo movement for n servos

  Note: Change numServos to number of servos and set servoPins to correct pins
*/
#include <Servo.h> 

//int servoPins[] = {9, 10};
//int servoPins[] = {2, 3, 4, 5};
int servoPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37};
//int servoPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31};
const int numServos = sizeof(servoPins)/sizeof(int);
Servo servos[numServos];
int myDelay = 10;

char serialData[numServos * 3];
char tempData[3];

void setup() {
  for (int i=0; i < numServos; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90);
  }
}

void loop() {
  int ang = 0;
  while (ang<45) {
    for (int i=0; i < numServos; i++) {
      servos[i].write(90+ang);
    }
    ang += 1;
    delay(myDelay);
  }
  while (ang>-45) {
    for (int i=0; i < numServos; i++) {
      servos[i].write(90+ang);
    }
    ang -= -1;
    delay(myDelay);
  }
  while (ang<0) {
    for (int i=0; i < numServos; i++) {
      servos[i].write(90+ang);
    }
    ang += 1;
    delay(myDelay);
  }
  
}
