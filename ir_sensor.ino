const int irPin = 2;

void setup() {
  pinMode(irPin, INPUT);
  Serial.begin(9600);
}

void loop() {

  int value = digitalRead(irPin);

  if (value == LOW) {
    Serial.println("Object Detected");
  }
  else {
    Serial.println("No Object");
  }

  delay(1000);
}