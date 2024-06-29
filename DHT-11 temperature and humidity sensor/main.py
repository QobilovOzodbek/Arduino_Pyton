import sys
import serial
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Temperature and Humidity Monitor')
        self.setGeometry(100, 100, 400, 250)
        self.setWindowIcon(QIcon('icon.png'))

        self.temp_label = QtWidgets.QLabel('Temperature: --', self)
        self.temp_label.setGeometry(50, 50, 300, 30)

        self.hum_label = QtWidgets.QLabel('Humidity: --', self)
        self.hum_label.setGeometry(50, 90, 300, 30)

        self.warning_label = QtWidgets.QLabel('', self)
        self.warning_label.setGeometry(50, 130, 300, 30)
        self.warning_label.setStyleSheet("color: red; font-size: 20px;")

        self.refresh_button = QtWidgets.QPushButton('Refresh Data', self)
        self.refresh_button.setGeometry(50, 170, 150, 30)
        self.refresh_button.clicked.connect(self.update_data)

        try:
            self.serial_port = serial.Serial('COM13', 9600, timeout=1)  # Arduino-ning COM portini tekshiring
        except serial.SerialException as e:
            QtWidgets.QMessageBox.critical(self, 'Serial Port Error', str(e))
            sys.exit(1)

    def update_data(self):
        line = self.serial_port.readline().decode('utf-8').strip()
        if line.startswith('Temperature:'):
            parts = line.split()
            temp = float(parts[1])
            hum = float(parts[3])
            
            self.temp_label.setText(f'Temperature: {temp}°C')
            self.hum_label.setText(f'Humidity: {hum}%')

            if temp > 33:
                self.warning_label.setText('Harorat oshishi')
            else:
                self.warning_label.setText('')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
