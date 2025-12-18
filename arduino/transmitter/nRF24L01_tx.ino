#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

struct DataPacket {
  int leftJoystickY;    // For coreless motor control
  int rightJoystickX;   // For Servo 1 control
  int rightJoystickY;   // For Servo 2 control
  
} data;

void setup() {
  Serial.begin(9600);
  radio.begin();
  
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void loop() {
  data.leftJoystickY = analogRead(A1);  // Left joystick Y-axis for motor control
  data.rightJoystickX = analogRead(A2); // Right joystick X-axis for Servo 1
  data.rightJoystickY = analogRead(A3); // Right joystick Y-axis for Servo 2

  if (!radio.write(&data, sizeof(data))) {
    Serial.println("Data sending failed");
  } else {
    Serial.println("Data sent successfully");
  }
  delay(100);
}
