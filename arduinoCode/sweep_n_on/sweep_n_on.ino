#include <Servo.h> 

//int servoPins[] = {2, 3, 4, 5, 6, 7};
int servoPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37};
//int lightPins[] = {8, 9, 10, 14, 15, 16};
const int numServos = sizeof(servoPins)/sizeof(int);
//const int numLights = sizeof(lightPins)/sizeof(int);
Servo servos[numServos];  // create servo object to control a servo 
                // a maximum of eight servo objects can be created  
int pos = 0;    // variable to store the servo position 
int act;
int opp;
int angles[] = {45,135};
 
void setup() {
  for (int i=0; i<numServos; i++) {
    servos[i].attach(servoPins[i]);  // attaches the servos on the pins 
  }
  
  /*
  for (int i=0; i<numLights; i++) {
    pinMode(lightPins[i],OUTPUT);  //set lights to output
    digitalWrite(lightPins[i], LOW); //make sure they are all off
  }
  */
  
  pos = 45;
  for (int i=0; i<numServos; i++) {
    servos[i].write(pos);              // tell servo to go to 90 
    delay(10);
  }
}

void loop() {
  /* continuous (not totally tested) IGNORE THIS
  if(pos == 360){pos = 0;}
  pos = pos + 180;
  act = int(45*sin(pos*(2*PI)/360) + 90);
  opp = int(-45*sin(pos*(2*PI)/360) + 90);
  
  servos[0].write(act);              // tell servo to go to position in variable 'pos'
  servos[2].write(act);
  servos[4].write(act);
  
  servos[1].write(opp);
  servos[3].write(opp);
  servos[5].write(opp);
  delay(100); 
  STOP IGNORING HERE */
  for(int i=0; i<2; i++) { //loop through angles (45 and -45)
    for(int j=0; j<numServos; j++) { //loop through emitters (servo+light)
      //digitalWrite(lightPins[j], HIGH); //turn light on 
      servos[j].write(angles[i]); //set servo to angle
      delay(100); //wait for servo to get there and light to turn on
    }
    //for(int j=0; j<numLights; j++) { //loop through all the lights (This block turns off all the lights)
    //  digitalWrite(lightPins[j], LOW); //turn the light off
    //}
  }
}
