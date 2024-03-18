#include <AccelStepper.h>   
int pos;             
int i;              
int t=0;   
const int DIR = 2;
const int STEP = 3;
int y = 50;
int x = 50;
#define motorInterfaceType 1
AccelStepper motor(motorInterfaceType, STEP, DIR);

void setup() {
  Serial.begin(9600);
  motor.setMaxSpeed(1000);
  motor.setAcceleration(500);
  motor.setSpeed(200);
  motor.moveTo(0);
  delay(2000);
  // motor.moveTo(50);
  // motor.run();
  // delay(1000);
}
void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'L') {
      motor.moveTo(motor.currentPosition() + 1);  
      motor.run();
    } else if (command == 'R') {
      motor.moveTo(motor.currentPosition() - 1);  
      motor.run();
    } else if (command == 'C') {
      motor.stop();
    }
  }
  Serial.flush();
  motor.run();
}  