import serial
import time

# Serial portni ochish
ser = serial.Serial('COM8', 9600)  # COM portni o'zgartirish kerak bo'lishi mumkin
time.sleep(2)  # Portni ochish uchun kutish

def save_to_file(data):
    with open('rfid_data.txt', 'a') as file:
        file.write(data + '\n')

print("RFID ma'lumotlarini o'qish uchun tayyor...")

try:
    while True:
        if ser.in_waiting > 0:
            rfid_data = ser.readline().decode('utf-8').strip()
            print(f"Kelgan ma'lumot: {rfid_data}")
            save_to_file(rfid_data)
except KeyboardInterrupt:
    print("Dasturni to'xtatildi.")
finally:
    ser.close()
