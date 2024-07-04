const int VRx = A0; // Joystikning x o'qi
const int VRy = A1; // Joystikning y o'qi
const int SW = 2;   // Joystikning tugmasi

void setup() {
  Serial.begin(9600);
  pinMode(SW, INPUT_PULLUP);
}

void loop() {
  int xPosition = analogRead(VRx);
  int yPosition = analogRead(VRy);
  int buttonState = digitalRead(SW);

  Serial.print("X:");
  Serial.print(xPosition);
  Serial.print(" Y:");
  Serial.print(yPosition);
  Serial.print(" Button:");
  Serial.println(buttonState);

  delay(100); // Har 100 ms da o'qish
}
