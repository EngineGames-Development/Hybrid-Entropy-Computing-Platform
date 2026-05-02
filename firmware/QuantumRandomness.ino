// --- Dual Photodiode Laser Entropy Generator ---

const int PIN_A = A0;
const int PIN_B = A1;
const int LASER_PIN = 7;

void setup() {
  Serial.begin(115200);

  pinMode(PIN_A, INPUT);
  pinMode(PIN_B, INPUT);

  pinMode(LASER_PIN, OUTPUT);
  digitalWrite(LASER_PIN, HIGH);

  analogReference(DEFAULT);
}

int sample_bit() {
  int a = analogRead(PIN_A);
  int b = analogRead(PIN_B);

  if (a > b) return 1;
  if (a < b) return 0;

  return -1;
}

int get_bit() {
  int bit = -1;

  for (int i = 0; i < 3; i++) {
    int s = sample_bit();
    if (s != -1) {
      bit = (bit == -1) ? s : (bit ^ s);
    }
    delayMicroseconds(50);
  }

  return bit;
}

void loop() {
  int bit = get_bit();

  if (bit == 0 || bit == 1) {
    Serial.print(bit);
  }

  delayMicroseconds(150);
}