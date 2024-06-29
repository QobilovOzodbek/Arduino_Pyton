#include "DHT.h"

#define DHTPIN 2     // DHT sensori ulangan pin
#define DHTTYPE DHT11   // Agar siz DHT22 ishlatayotgan bo'lsangiz, DHT22 ni ishlating

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" Humidity: ");
  Serial.println(h);

  delay(2000); // 2 soniya kutish
}
