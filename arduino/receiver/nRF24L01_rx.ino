#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

struct DataPacket {
  int leftJoystickY;
  int rightJoystickX;
  int rightJoystickY;
} data;

Servo servo1; // Servo for right joystick X-axis
Servo servo2; // Servo for right joystick Y-axis

const int motorPin = 9; // Coreless motor connected to IRF520 gate
const int motorThreshold = 600; // Adjust threshold based on testing

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_LOW);
  radio.startListening();

  servo1.attach(5); // Connect Servo 1 to pin D3
  servo2.attach(6); // Connect Servo 2 to pin D5
  pinMode(motorPin, OUTPUT);
}

void loop() {
  if (radio.available()) {
    radio.read(&data, sizeof(data));
    
    // Coreless Motor Control - Adjust speed based on joystick position
    int motorSpeed = map(data.leftJoystickY, 0, 1023, 0, 255);
    if (data.leftJoystickY > motorThreshold) {
      analogWrite(motorPin, motorSpeed);
    } else {
      analogWrite(motorPin, 0); // Stop motor if below threshold
    }
    
    // Servo 1 Control (Horizontal direction)
    int servo1Pos = map(data.rightJoystickX, 0, 1023, 0, 180);
    servo1.write(servo1Pos);
    
    // Servo 2 Control (Vertical direction)
    int servo2Pos = map(data.rightJoystickY, 0, 1023, 0, 180);
    servo2.write(servo2Pos);

    // Print values to Serial Monitor for debugging
    Serial.print("Motor Speed: ");
    Serial.print(motorSpeed);
    Serial.print(" | Servo 1 Pos: ");
    Serial.print(servo1Pos);
    Serial.print(" | Servo 2 Pos: ");
    Serial.println(servo2Pos);
  }
  delay(50);
}
