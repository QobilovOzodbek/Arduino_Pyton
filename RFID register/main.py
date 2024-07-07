import sys
import sqlite3
import serial
from PyQt5 import QtWidgets, QtCore

class RFIDRegisterApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initDB()
        self.initSerial()

    def initUI(self):
        self.setWindowTitle('RFID Register')
        self.setGeometry(100, 100, 400, 300)
        
        self.label = QtWidgets.QLabel('RFID Teggizing', self)
        self.label.setGeometry(50, 20, 200, 30)
        
        self.viewButton = QtWidgets.QPushButton('Ro\'yxatni ko\'rish', self)
        self.viewButton.setGeometry(250, 20, 120, 30)
        self.viewButton.clicked.connect(self.viewDatabase)
        
        self.userList = QtWidgets.QListWidget(self)
        self.userList.setGeometry(50, 60, 320, 200)
        
        self.show()

    def initDB(self):
        self.conn = sqlite3.connect('rfid_users.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          uid TEXT UNIQUE,
                          name TEXT,
                          surname TEXT)''')
        self.conn.commit()

    def initSerial(self):
        self.serialPort = serial.Serial('COM12', 9600, timeout=1)  # Bu yerda port raqamini o'zgartiring
        self.serialPort.flush()
        self.serialThread = QtCore.QThread()
        self.serialWorker = SerialWorker(self.serialPort)
        self.serialWorker.moveToThread(self.serialThread)
        self.serialThread.started.connect(self.serialWorker.run)
        self.serialWorker.uidReceived.connect(self.handleUID)
        self.serialThread.start()

    def handleUID(self, uid):
        uid = uid.strip()
        self.c.execute("SELECT * FROM users WHERE uid=?", (uid,))
        result = self.c.fetchone()
        
        if result:
            QtWidgets.QMessageBox.information(self, "Ma'lumot", "Bu karta mavjud")
        else:
            self.registerUser(uid)

    def registerUser(self, uid):
        name, okPressed = QtWidgets.QInputDialog.getText(self, "Ism", "Ismingizni kiriting:")
        if okPressed and name:
            surname, okPressed = QtWidgets.QInputDialog.getText(self, "Familiya", "Familiyangizni kiriting:")
            if okPressed and surname:
                self.c.execute("INSERT INTO users (uid, name, surname) VALUES (?, ?, ?)", (uid, name, surname))
                self.conn.commit()
                QtWidgets.QMessageBox.information(self, "Ma'lumot", "Foydalanuvchi ro'yxatga olindi")
                self.updateUserList()

    def updateUserList(self):
        self.userList.clear()
        self.c.execute("SELECT name, surname FROM users")
        for row in self.c.fetchall():
            self.userList.addItem(f"{row[0]} {row[1]}")

    def viewDatabase(self):
        self.updateUserList()
        self.showAllUsers()

    def showAllUsers(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Barcha foydalanuvchilar")
        layout = QtWidgets.QVBoxLayout(dialog)

        table = QtWidgets.QTableWidget(dialog)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Id", "Ism", "Familiya", "UID"])

        self.c.execute("SELECT id, name, surname, uid FROM users")
        rows = self.c.fetchall()
        table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()

class SerialWorker(QtCore.QObject):
    uidReceived = QtCore.pyqtSignal(str)

    def __init__(self, serialPort):
        super().__init__()
        self.serialPort = serialPort

    def run(self):
        while True:
            if self.serialPort.in_waiting > 0:
                uid = self.serialPort.readline().decode('utf-8').strip()
                if uid.startswith("UID:"):
                    uid = uid[4:]
                    self.uidReceived.emit(uid)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = RFIDRegisterApp()
    sys.exit(app.exec_())
