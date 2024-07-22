import tkinter as tk
from tkinter import ttk
import serial
import time

# Arduino bilan aloqa o'rnatish
arduino = serial.Serial('COM12', 9600, timeout=1)
time.sleep(2)  # Arduino bilan aloqa o'rnatish uchun kutish

# Oldingi burchak
previous_angle = None

# Servo burchagini o'zgartirish funksiyasi
def set_servo_angle(angle):
    global previous_angle
    if previous_angle != angle:  # Faqat burchak o'zgarganda
        arduino.write(f"{angle}\n".encode())
        previous_angle = angle
        time.sleep(0.1)

# Burchakni yangilash funksiyasi
def update_servo_angle(event=None):
    angle = angle_var.get()
    if angle.isdigit():
        angle = int(angle)
        if 0 <= angle <= 180:
            set_servo_angle(angle)

# Interfeys yaratish
root = tk.Tk()
root.title("Servo Boshqaruvi")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

angle_var = tk.StringVar()

# Burchakni kiritish uchun kirish joyi
angle_entry = ttk.Entry(mainframe, width=7, textvariable=angle_var)
angle_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

# Burchakni kiritish uchun label
ttk.Label(mainframe, text="Burchak (0-180):").grid(column=0, row=1, sticky=(tk.W, tk.E))

# Enter tugmasini bosganda burchakni yangilash
angle_entry.bind('<Return>', update_servo_angle)

# Kiritish joyiga fokus berish
angle_entry.focus()

# Layout konfiguratsiya qilish
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
