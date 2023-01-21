int RPWM = 5;
int LPWM = 6;
int REN = 7;
int LEN = 8;

void forward() {
  digitalWrite(REN, HIGH);
  digitalWrite(LEN, HIGH);
  delay(100);
  for (int i = 0; i < 256; i++) {
    analogWrite(RPWM, i);
    analogWrite(LPWM, 255 - i);
    delay(100);
    digitalWrite(REN, LOW);
    digitalWrite(LEN, LOW);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(REN, OUTPUT);
  pinMode(LEN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String state = Serial.readStringUntil('\n');
    if (state == "forward") {
      digitalWrite(13, HIGH);
      state = "done";
      delay(1000);
      digitalWrite(13, LOW);
      forward();
    }
  }
}
