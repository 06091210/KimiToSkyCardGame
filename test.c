int stepPin = 3;
int dirPin = 4;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  // 正回転
  digitalWrite(dirPin, HIGH);

  for (int i = 0; i < 200; i++) { // 200ステップ = 1回転（一般的）
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(800);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(800);
  }

  delay(1000);

  // 逆回転
  digitalWrite(dirPin, LOW);

  for (int i = 0; i < 200; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(800);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(800);
  }

  delay(1000);
}
