#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>
#include <nRF24L01.h>
#include <RF24.h>

// LCD ekran uchun
LiquidCrystal_I2C lcd(0x27, 16, 2);

// RFID
#define SS_PIN 2 // GPIO2
#define RST_PIN 0 // GPIO0
MFRC522 rfid(SS_PIN, RST_PIN);

// NRF24L01
RF24 radio(4, 5); // CE: GPIO4, CSN: GPIO5
const byte address[6] = "00001";

// RX470C-V01
const int signalPin1 = 16; // GPIO16
const int signalPin2 = 17; // GPIO17

void setup() {
  // LCD initialization
  lcd.begin(2,16);
  lcd.print("Starting...");

  // RFID initialization
  SPI.begin();
  rfid.PCD_Init();
  Serial.begin(9600);
  
  // NRF24L01 initialization
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  
  // RX470C-V01 initialization
  pinMode(signalPin1, INPUT);
  pinMode(signalPin2, INPUT);

  lcd.clear();
  lcd.print("System Ready");
}

void loop() {
  // RFID reading
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    lcd.clear();
    lcd.print("RFID Tag:");
    for (byte i = 0; i < rfid.uid.size; i++) {
      lcd.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
      lcd.print(rfid.uid.uidByte[i], HEX);
    }
    lcd.setCursor(0, 1);
    lcd.print("Read");
    rfid.PICC_HaltA();
    delay(2000);
    lcd.clear();
    lcd.print("System Ready");
  }

  // NRF24L01 listening
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    lcd.clear();
    lcd.print("NRF Data:");
    lcd.setCursor(0, 1);
    lcd.print(text);
    delay(2000);
    lcd.clear();
    lcd.print("System Ready");
  }

  // RX470C-V01 signal handling
  int signal1 = digitalRead(signalPin1);
  int signal2 = digitalRead(signalPin2);
  if (signal1 == HIGH || signal2 == HIGH) {
    lcd.clear();
    lcd.print("Signal Detected");
    lcd.setCursor(0, 1);
    lcd.print(signal1 == HIGH ? "Sig1 HIGH " : "");
    lcd.print(signal2 == HIGH ? "Sig2 HIGH" : "");
    delay(2000);
    lcd.clear();
    lcd.print("System Ready");
  }
}
