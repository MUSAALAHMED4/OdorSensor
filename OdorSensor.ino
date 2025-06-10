const int mq135Pin = A0;

void setup() {
  Serial.begin(9600);  // تفعيل الاتصال التسلسلي
}

void loop() {
  int value = analogRead(mq135Pin);  // قراءة من الحساس
  value = map(value, 0, 1023, 0, 100);  // تحجيم إلى 0-100
  unsigned long timeNow = millis();
  String smellType = detectSmell(value);

  Serial.print(timeNow);
  Serial.print(",");
  Serial.print(value);
  Serial.print(",");
  Serial.println(smellType);

  delay(2000);  // قراءة كل ثانيتين
}

String detectSmell(int val) {
  if (val >= 31 && val <= 55) {
    return "Alkol";
  } else if (val > 55 && val <= 80) {
    return "Sarımsak";
  } else if (val > 80 && val <= 100) {
    return "Duman";
  } else if (val >= 10 && val < 31) {
    return "Temiz Hava";
  } else {
    return "Bekleniyor...";
  }
}
