import serial

def read_rfid(serial_port='COM13', baud_rate=9600):
    ser = serial.Serial(serial_port, baud_rate)
    while True:
        if ser.in_waiting > 0:
            rfid_data = ser.readline().decode('utf-8').strip()
            print(f"RFID Data: {rfid_data}")
            save_rfid_data(rfid_data)

def save_rfid_data(rfid_data):
    with open('rfid_data.txt', 'a') as file:
        file.write(rfid_data + '\n')

if __name__ == '__main__':
    read_rfid()
